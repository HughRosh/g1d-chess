#!/usr/bin/env python3

from pathlib import Path
import sys
import chess

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.chess_engine import choose_move
from src.utils import load_config
from perception.factory import make_board_recognizer
from hardware.g1d.factory import make_g1d_controller
from planning.chess_plan import make_chess_move_plan
from planning.executor import execute_commands


def main():
    scene = load_config("configs/scene.yaml")["scene"]

    recognizer = make_board_recognizer("mock")
    fen = recognizer.recognize()

    print("FEN:")
    print(fen)

    board = chess.Board(fen)
    move = choose_move(board)

    print("Chosen move:", move.uci())

    robot = make_g1d_controller("mock")
    commands = make_chess_move_plan(move.uci(), scene)

    execute_commands(robot, commands, use_ik=False)

    print("Perception-to-chess mock pipeline complete")


if __name__ == "__main__":
    main()
