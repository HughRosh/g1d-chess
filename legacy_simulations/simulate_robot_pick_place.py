#!/usr/bin/env python3

import sys
import time
from pathlib import Path

import chess
import mujoco
import mujoco.viewer
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils import load_config
from scripts.create_chess_piece_scene import square_xy, starting_pieces

MODEL_PATH = "simulation/mujoco/chess_piece_scene.xml"


def set_free_joint(model, data, joint_name, x, y, z):
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)
    if jid < 0:
        return False

    qadr = model.jnt_qposadr[jid]
    data.qpos[qadr:qadr + 7] = [x, y, z, 1, 0, 0, 0]
    return True


def piece_pose(square, scene):
    table = scene["table"]
    board = scene["board"]
    x, y = square_xy(square, scene)
    z = table["height_m"] + board["thickness_m"] + 0.055 / 2.0
    return x, y, z


def side_pose(count, scene, color):
    table = scene["table"]
    board = scene["board"]

    x = table["x_m"] + 0.38
    y0 = table["y_m"] - 0.32 if color == chess.WHITE else table["y_m"] + 0.18
    y = y0 + 0.04 * count
    z = table["height_m"] + board["thickness_m"] + 0.055 / 2.0
    return x, y, z


def interpolate(a, b, steps=90):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    for s in np.linspace(0, 1, steps):
        yield ((1 - s) * a + s * b).tolist()


def sync(viewer, model, data, dt=0.012):
    mujoco.mj_forward(model, data)
    viewer.sync()
    time.sleep(dt)


def move_gripper(viewer, model, data, start, end, carried_square=None):
    for x, y, z in interpolate(start, end, 100):
        set_free_joint(model, data, "gripper_marker_free", x, y, z)

        if carried_square is not None:
            set_free_joint(model, data, f"piece_{carried_square}_free", x, y, z - 0.07)

        sync(viewer, model, data)


def pick_and_place(viewer, model, data, scene, board, from_sq, to_xyz, carried_square):
    table = scene["table"]
    board_cfg = scene["board"]

    rest = [table["x_m"] - 0.35, table["y_m"] - 0.35, table["height_m"] + 0.45]

    sx, sy, sz = piece_pose(from_sq, scene)
    tx, ty, tz = to_xyz

    hover_from = [sx, sy, sz + 0.18]
    grasp_from = [sx, sy, sz + 0.06]
    hover_to = [tx, ty, tz + 0.18]
    place_to = [tx, ty, tz + 0.06]

    print("  rest -> hover")
    move_gripper(viewer, model, data, rest, hover_from)

    print("  descend")
    move_gripper(viewer, model, data, hover_from, grasp_from)

    print("  close gripper / attach")
    time.sleep(0.3)

    print("  lift")
    move_gripper(viewer, model, data, grasp_from, hover_from, carried_square)

    print("  travel")
    move_gripper(viewer, model, data, hover_from, hover_to, carried_square)

    print("  descend to place")
    move_gripper(viewer, model, data, hover_to, place_to, carried_square)

    print("  open gripper / detach")
    set_free_joint(model, data, f"piece_{carried_square}_free", tx, ty, tz)
    sync(viewer, model, data)
    time.sleep(0.3)

    print("  retreat")
    move_gripper(viewer, model, data, place_to, hover_to)

    print("  return home")
    move_gripper(viewer, model, data, hover_to, rest)


def reset_board(model, data, scene):
    for sq in starting_pieces():
        x, y, z = piece_pose(sq, scene)
        set_free_joint(model, data, f"piece_{sq}_free", x, y, z)


def main():
    scene = load_config("configs/scene.yaml")["scene"]

    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    board = chess.Board()

    moves = [
        "e2e4",
        "e7e5",
        "g1f3",
        "b8c6",
        "f1b5",
        "a7a6",
        "b5c6",
    ]

    white_captures = 0
    black_captures = 0

    print("Human is White. Robot is Black.")
    print("Robot rests between moves.")
    print("Captured pieces are moved to side capture zones.")
    print("Board resets after game over.")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        reset_board(model, data, scene)
        sync(viewer, model, data)

        for uci in moves:
            if not viewer.is_running():
                break

            move = chess.Move.from_uci(uci)
            from_sq = chess.square_name(move.from_square)
            to_sq = chess.square_name(move.to_square)

            print("\nMove:", uci)
            print("Actor:", "Human white" if board.turn == chess.WHITE else "Robot black")

            if board.is_capture(move):
                victim_color = not board.turn
                capture_target = side_pose(
                    white_captures if victim_color == chess.WHITE else black_captures,
                    scene,
                    victim_color,
                )

                if victim_color == chess.WHITE:
                    white_captures += 1
                else:
                    black_captures += 1

                print("Capture:", to_sq, "-> side table")
                pick_and_place(
                    viewer,
                    model,
                    data,
                    scene,
                    board,
                    to_sq,
                    capture_target,
                    to_sq,
                )

            destination = piece_pose(to_sq, scene)

            print("Move piece:", from_sq, "->", to_sq)
            pick_and_place(
                viewer,
                model,
                data,
                scene,
                board,
                from_sq,
                destination,
                from_sq,
            )

            board.push(move)

            print(board)

            if board.is_game_over():
                print("Game over:", board.result())
                print("Resetting board.")
                board.reset()
                reset_board(model, data, scene)
                break

        print("\nDemo complete. Viewer stays open.")
        while viewer.is_running():
            viewer.sync()
            time.sleep(0.03)


if __name__ == "__main__":
    main()
