#!/usr/bin/env python3

import sys
from pathlib import Path
import chess

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils import load_config
from src.chess_engine import choose_move
from hardware.g1d.factory import make_g1d_controller
from planning.chess_plan import make_chess_move_plan
from planning.executor import execute_commands


def reset_board():
    print("\nGame over. Reset the physical board to the starting position.")
    return chess.Board()


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    robot = make_g1d_controller("mock")
    board = chess.Board()

    print("You are White. Robot is Black.")
    print("Enter moves like e2e4. Type quit to exit.\n")

    while True:
        print(board)

        if board.is_game_over():
            print("Result:", board.result())
            board = reset_board()
            continue

        human = input("\nYour move: ").strip()

        if human == "quit":
            break

        try:
            move = chess.Move.from_uci(human)
        except ValueError:
            print("Invalid format.")
            continue

        if move not in board.legal_moves:
            print("Illegal move.")
            continue

        board.push(move)

        if board.is_game_over():
            print("Result:", board.result())
            board = reset_board()
            continue

        robot_move = choose_move(board)
        print("Robot move:", robot_move.uci())

        commands = make_chess_move_plan(robot_move.uci(), scene)
        execute_commands(robot, commands, use_ik=False)

        board.push(robot_move)


if __name__ == "__main__":
    main()
