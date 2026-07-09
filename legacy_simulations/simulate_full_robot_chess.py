#!/usr/bin/env python3

import sys
import time
from pathlib import Path
import numpy as np
import chess
import mujoco
import mujoco.viewer

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils import load_config
from planning.chess_plan import make_chess_move_plan, square_to_xyz
from robot.kinematics.pinocchio_solver import G1DKinematics
from robot.kinematics.controller_mapping import pin_q_to_dual_arm_q
from scripts.create_robot_chess_scene import square_xy, starting_squares

MODEL_PATH = "simulation/urdf/g1d_chess_robot_piece_scene.urdf"

# Offset from Dex1 base frame to the approximate grasp point.
# Isaac Sim's pick-place example uses the same idea: tune end_effector_offset.
EE_TO_PIECE_Z = -0.06
GRASP_CLEARANCE = 0.09
HOVER_CLEARANCE = 0.28

RIGHT_ARM_JOINTS = [
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
]

LEFT_ARM_JOINTS = [
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
]

LEFT_ARM_SAFE_HOME = [
    -0.30,
     0.75,
     0.00,
     0.95,
     0.00,
     0.20,
     0.00,
]

RIGHT_WRIST_TOP_DOWN = {
    "right_wrist_roll_joint": 0.0,
    "right_wrist_pitch_joint": 0.55,
    "right_wrist_yaw_joint": 0.0,
}


def set_joint(model, data, name, value):
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
    if jid < 0:
        return
    qadr = model.jnt_qposadr[jid]
    data.qpos[qadr] = value


def set_right_arm(model, data, dual_arm_q):
    right_q = list(dual_arm_q[7:14])

    # Force a better visual gripper orientation after position IK.
    for i, name in enumerate(RIGHT_ARM_JOINTS):
        if name in RIGHT_WRIST_TOP_DOWN:
            right_q[i] = RIGHT_WRIST_TOP_DOWN[name]

    for name, value in zip(RIGHT_ARM_JOINTS, right_q):
        set_joint(model, data, name, value)


def set_left_arm_safe(model, data):
    for name, value in zip(LEFT_ARM_JOINTS, LEFT_ARM_SAFE_HOME):
        set_joint(model, data, name, value)


def set_piece(model, data, square, x, y, z):
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, f"piece_{square}_free")
    if jid < 0:
        return False
    qadr = model.jnt_qposadr[jid]
    data.qpos[qadr:qadr + 7] = [x, y, z, 1, 0, 0, 0]
    return True


def piece_z(scene):
    return scene["table"]["height_m"] + scene["board"]["thickness_m"] + 0.055 / 2.0


def reset_board(model, data, scene):
    z = piece_z(scene)
    for sq in starting_squares():
        x, y = square_xy(sq, scene)
        set_piece(model, data, sq, x, y, z)


def side_capture_pose(count, color, scene):
    table = scene["table"]
    z = piece_z(scene)

    x = table["x_m"] + 0.38
    y0 = table["y_m"] - 0.33 if color == chess.WHITE else table["y_m"] + 0.22
    y = y0 + 0.04 * count

    return x, y, z


def interpolate(q0, q1, steps=90):
    q0 = np.asarray(q0, dtype=float)
    q1 = np.asarray(q1, dtype=float)
    for a in np.linspace(0, 1, steps):
        yield ((1 - a) * q0 + a * q1).tolist()


def sync(model, data, viewer, dt=0.012):
    mujoco.mj_forward(model, data)
    viewer.sync()
    time.sleep(dt)


def current_right_ee_xyz(pin_kin, pin_q):
    fk = pin_kin.forward_kinematics(pin_q)
    return np.asarray(fk["position_xyz"], dtype=float)


def solve_plan_ik(scene, move_uci):
    kin = G1DKinematics()
    commands = make_chess_move_plan(move_uci, scene)

    out = []

    for cmd in commands:
        if cmd.action == "move_pose":
            # Convert desired piece/grasp position into desired Dex1 base position.
            target = np.asarray(cmd.target.position_xyz, dtype=float)

            if "hover" in cmd.note or "lift" in cmd.note or "retreat" in cmd.note or "move above" in cmd.note:
                target[2] += HOVER_CLEARANCE
            else:
                target[2] += GRASP_CLEARANCE

            # The piece is below the Dex1 base frame, so raise the IK target.
            target[2] -= EE_TO_PIECE_Z

            q, ok, iters, err = kin.solve_position_ik(target)
            print(f"  {cmd.note}: position IK ok={ok}, err={err:.5f}")

            if ok:
                out.append((cmd, pin_q_to_dual_arm_q(kin.model, q), q, kin))

        else:
            out.append((cmd, None, None, kin))

    return out

def play_robot_move(model, data, viewer, scene, board, move_uci, capture_counts):
    from_sq = move_uci[:2]
    to_sq = move_uci[2:4]
    z = piece_z(scene)

    print("\nMove:", move_uci)
    print("Actor:", "Human white" if board.turn == chess.WHITE else "Robot black")

    if board.is_capture(chess.Move.from_uci(move_uci)):
        victim_color = not board.turn
        count = capture_counts["white" if victim_color == chess.WHITE else "black"]

        cx, cy, cz = side_capture_pose(count, victim_color, scene)
        capture_counts["white" if victim_color == chess.WHITE else "black"] += 1

        print("Capture:", to_sq, "-> side table")
        tx, ty, _ = square_to_xyz(to_sq, scene)
        animate_piece_only(model, data, viewer, to_sq, (tx, ty, z), (cx, cy, cz))

    plan = solve_plan_ik(scene, move_uci)

    q_current = np.zeros(14)
    carrying = False

    last_pin_q = None
    last_kin = None

    for cmd, q_target, pin_q_target, kin in plan:
        if cmd.action == "close_gripper":
            print("  close gripper / attach piece")
            carrying = True
            time.sleep(0.3)
            continue

        if cmd.action == "open_gripper":
            print("  open gripper / release piece")
            tx, ty, _ = square_to_xyz(to_sq, scene)
            set_piece(model, data, from_sq, tx, ty, z)
            carrying = False
            sync(model, data, viewer)
            time.sleep(0.3)
            continue

        if q_target is None:
            continue

        for step_i, q in enumerate(interpolate(q_current, q_target)):
            set_left_arm_safe(model, data)
            set_right_arm(model, data, q)

            # During carry, piece follows the actual IK/FK end-effector path.
            if carrying and last_pin_q is not None and pin_q_target is not None:
                a = step_i / 89.0
                pin_q_interp = (1 - a) * np.asarray(last_pin_q) + a * np.asarray(pin_q_target)
                # Piece follows actual end-effector FK, not an independent planned lift.
                ee = current_right_ee_xyz(kin, pin_q_interp)
                set_piece(model, data, from_sq, ee[0], ee[1], ee[2] + EE_TO_PIECE_Z)

            sync(model, data, viewer)

        q_current = q_target
        last_pin_q = pin_q_target
        last_kin = kin

    board.push(chess.Move.from_uci(move_uci))
    print(board)


def current_piece_xyz(model, data, square):
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, f"piece_{square}_free")
    qadr = model.jnt_qposadr[jid]
    return data.qpos[qadr:qadr + 3].copy()


def animate_piece_only(model, data, viewer, square, start, end):
    for a in np.linspace(0, 1, 100):
        p = (1 - a) * np.asarray(start) + a * np.asarray(end)
        p[2] += 0.06 * np.sin(np.pi * a)
        set_piece(model, data, square, p[0], p[1], p[2])
        sync(model, data, viewer)


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    board = chess.Board()

    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6", "b5c6"]

    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    capture_counts = {"white": 0, "black": 0}

    print("Full robot + piece chess simulation.")
    print("Robot plays Black / second move.")
    print("Captured pieces go to side zones.")
    print("Board resets if game ends.")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        reset_board(model, data, scene)
        set_left_arm_safe(model, data)
        sync(model, data, viewer)

        for move in moves:
            if not viewer.is_running():
                break

            play_robot_move(model, data, viewer, scene, board, move, capture_counts)

            if board.is_game_over():
                print("Game over:", board.result())
                print("Resetting board.")
                board.reset()
                reset_board(model, data, scene)
                break

        print("Demo complete. Viewer stays open.")
        while viewer.is_running():
            viewer.sync()
            time.sleep(0.03)


if __name__ == "__main__":
    main()
