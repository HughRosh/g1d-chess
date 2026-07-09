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
from scripts.create_chess_piece_scene import square_xy, starting_pieces

MODEL_PATH = "simulation/mujoco/chess_piece_scene.xml"


def set_piece(model, data, square, x, y, z):
    joint = f"piece_{square}_free"
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, joint)
    if jid < 0:
        return False
    qadr = model.jnt_qposadr[jid]
    data.qpos[qadr:qadr + 7] = [x, y, z, 1, 0, 0, 0]
    return True


def animate_piece(model, data, viewer, square, start, end, lift=0.10):
    sx, sy, sz = start
    ex, ey, ez = end

    for a in np.linspace(0, 1, 140):
        x = (1 - a) * sx + a * ex
        y = (1 - a) * sy + a * ey
        z = (1 - a) * sz + a * ez + lift * np.sin(np.pi * a)

        set_piece(model, data, square, x, y, z)

        mujoco.mj_forward(model, data)
        viewer.sync()
        time.sleep(0.012)


def side_capture_xy(count, scene):
    table = scene["table"]
    x = table["x_m"] + 0.38
    y = table["y_m"] - 0.32 + 0.04 * count
    return x, y


def reset_all_pieces(model, data, scene, piece_z):
    for sq in starting_pieces():
        x, y = square_xy(sq, scene)
        set_piece(model, data, sq, x, y, piece_z)
    mujoco.mj_forward(model, data)


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    table = scene["table"]
    board_cfg = scene["board"]

    piece_z = table["height_m"] + board_cfg["thickness_m"] + 0.055 / 2.0

    board = chess.Board()

    # Includes a capture: Bxc6
    moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6", "b5c6"]

    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    capture_count = 0

    print("Human is White. Robot is Black.")
    print("Robot always makes the second move.")
    print("Captured pieces move to the side of the table.")
    print("Board resets at game over.")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        reset_all_pieces(model, data, scene, piece_z)

        for uci in moves:
            if not viewer.is_running():
                break

            move = chess.Move.from_uci(uci)
            from_sq = chess.square_name(move.from_square)
            to_sq = chess.square_name(move.to_square)

            print("\nMove:", uci)
            print("Turn:", "Human white" if board.turn == chess.WHITE else "Robot black")
            print("Rest position between moves")

            sx, sy = square_xy(from_sq, scene)
            ex, ey = square_xy(to_sq, scene)

            if board.is_capture(move):
                captured_sq = to_sq
                cx, cy = side_capture_xy(capture_count, scene)
                capture_count += 1

                print("Capture:", captured_sq, "to side table")
                animate_piece(
                    model,
                    data,
                    viewer,
                    captured_sq,
                    (ex, ey, piece_z),
                    (cx, cy, piece_z),
                    lift=0.06,
                )

            print("Move piece:", from_sq, "to", to_sq)
            animate_piece(
                model,
                data,
                viewer,
                from_sq,
                (sx, sy, piece_z),
                (ex, ey, piece_z),
                lift=0.10,
            )

            board.push(move)

            time.sleep(0.6)

            if board.is_game_over():
                print("Game over:", board.result())
                print("Resetting board")
                board.reset()
                reset_all_pieces(model, data, scene, piece_z)
                break

        print("\nDemo complete. Press Quit in MuJoCo to close.")
        while viewer.is_running():
            viewer.sync()
            time.sleep(0.03)


if __name__ == "__main__":
    main()
