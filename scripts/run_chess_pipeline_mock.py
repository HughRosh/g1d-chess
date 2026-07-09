#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from src.board_detector import detect_board_state
from src.chess_engine import choose_move
from hardware.g1d.factory import make_g1d_controller
from planning.chess_plan import make_chess_move_plan
from planning.executor import execute_commands


def main():
    scene = load_config("configs/scene.yaml")["scene"]

    board = detect_board_state()
    move = choose_move(board)

    print("Chosen chess move:", move.uci())

    robot = make_g1d_controller("mock")
    commands = make_chess_move_plan(move.uci(), scene)

    execute_commands(robot, commands)

    print("Mock chess pipeline complete")


if __name__ == "__main__":
    main()
