#!/usr/bin/env python3

from pathlib import Path
import sys
import argparse
import chess

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from src.chess_engine import choose_move
from vision.camera import Camera
from perception.factory import make_board_recognizer
from hardware.g1d.factory import make_g1d_controller
from planning.chess_plan import make_chess_move_plan
from planning.executor import execute_commands
from planning.safety_gate import require_real_robot_confirmation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default="mock", choices=["mock", "real"])
    parser.add_argument("--recognizer", default="mock", choices=["mock", "chesscog"])
    parser.add_argument("--camera", type=int, default=None)
    parser.add_argument("--interface", default="eth0")
    parser.add_argument("--use-ik", action="store_true")
    parser.add_argument("--allow-real", action="store_true")
    args = parser.parse_args()

    require_real_robot_confirmation(args.backend, args.allow_real)

    scene = load_config("configs/scene.yaml")["scene"]

    frame = None
    if args.camera is not None:
        cam = Camera(index=args.camera)
        frame = cam.read()
        cam.release()

    recognizer = make_board_recognizer(args.recognizer)
    fen = recognizer.recognize(frame)

    print("Recognized FEN:")
    print(fen)

    board = chess.Board(fen)
    move = choose_move(board)

    print("Chosen move:", move.uci())

    robot = make_g1d_controller(
        backend=args.backend,
        interface=args.interface,
    )

    commands = make_chess_move_plan(move.uci(), scene)

    execute_commands(
        robot,
        commands,
        use_ik=args.use_ik,
    )

    print("Autonomous chess pipeline complete")


if __name__ == "__main__":
    main()
