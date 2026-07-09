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
from scripts.create_robot_chess_scene import square_xy, starting_squares

MODEL_PATH = "simulation/urdf/g1d_chess_robot_piece_scene.urdf"

RIGHT_ARM = [
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
]

HOME = [-0.65, -0.15, 0.0, 0.40, 0.0, 0.75, 0.0]
PICK = [-0.85, -0.25, 0.15, 0.45, 0.0, 0.85, 0.0]
PLACE = [-0.75, -0.10, -0.25, 0.45, 0.0, 0.85, 0.0]


def set_joint(model, data, name, value):
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
    if jid < 0:
        print("Missing joint:", name)
        return
    data.qpos[model.jnt_qposadr[jid]] = value


def set_arm(model, data, q):
    for name, val in zip(RIGHT_ARM, q):
        set_joint(model, data, name, val)


def set_piece(model, data, sq, x, y, z):
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, f"piece_{sq}_free")
    if jid < 0:
        print("Missing piece joint:", sq)
        return
    a = model.jnt_qposadr[jid]
    data.qpos[a:a+7] = [x, y, z, 1, 0, 0, 0]


def piece_pose(sq, scene):
    x, y = square_xy(sq, scene)
    z = scene["table"]["height_m"] + scene["board"]["thickness_m"] + 0.055 / 2
    return x, y, z


def reset_pieces(model, data, scene):
    for sq in starting_squares():
        set_piece(model, data, sq, *piece_pose(sq, scene))


def lerp(a, b, n=100):
    a = np.array(a)
    b = np.array(b)
    for t in np.linspace(0, 1, n):
        yield ((1 - t) * a + t * b).tolist(), t


def animate_arm(model, data, viewer, q0, q1, carried=None, start=None, end=None):
    for q, t in lerp(q0, q1):
        set_arm(model, data, q)

        if carried and start and end:
            p0 = np.array(start)
            p1 = np.array(end)
            p = (1 - t) * p0 + t * p1
            p[2] += 0.08 * np.sin(np.pi * t)
            set_piece(model, data, carried, p[0], p[1], p[2])

        mujoco.mj_forward(model, data)
        viewer.sync()
        time.sleep(0.012)


def side_capture_pose(count, scene):
    table = scene["table"]
    z = scene["table"]["height_m"] + scene["board"]["thickness_m"] + 0.055 / 2
    return table["x_m"] + 0.38, table["y_m"] - 0.30 + 0.04 * count, z


def do_move(model, data, viewer, scene, board, move_uci, capture_count):
    move = chess.Move.from_uci(move_uci)
    fsq = chess.square_name(move.from_square)
    tsq = chess.square_name(move.to_square)

    print("\nMove:", move_uci)
    print("Actor:", "Human white" if board.turn == chess.WHITE else "Robot black")

    if board.is_capture(move):
        print("Capture:", tsq, "to side table")
        animate_arm(model, data, viewer, HOME, PICK)
        animate_arm(
            model, data, viewer, PICK, PLACE,
            carried=tsq,
            start=piece_pose(tsq, scene),
            end=side_capture_pose(capture_count, scene),
        )
        animate_arm(model, data, viewer, PLACE, HOME)
        capture_count += 1

    print("Pick/place:", fsq, "->", tsq)
    animate_arm(model, data, viewer, HOME, PICK)
    animate_arm(
        model, data, viewer, PICK, PLACE,
        carried=fsq,
        start=piece_pose(fsq, scene),
        end=piece_pose(tsq, scene),
    )
    animate_arm(model, data, viewer, PLACE, HOME)

    board.push(move)
    print(board)

    return capture_count


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    board = chess.Board()
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6", "b5c6"]

    capture_count = 0

    print("Visual chess simulator")
    print("Robot rests between moves.")
    print("Captured pieces move to the side.")
    print("Robot is Black / second move.")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        reset_pieces(model, data, scene)
        set_arm(model, data, HOME)
        mujoco.mj_forward(model, data)
        viewer.sync()

        for m in moves:
            if not viewer.is_running():
                break
            capture_count = do_move(model, data, viewer, scene, board, m, capture_count)

        print("Demo complete. Viewer stays open.")
        while viewer.is_running():
            viewer.sync()
            time.sleep(0.03)


if __name__ == "__main__":
    main()
