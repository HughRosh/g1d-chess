#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from hardware.g1d.factory import make_g1d_controller
from planning.executor import execute_commands
from planning.cup_plan import make_cup_pick_drop_plan
from planning.chess_plan import make_chess_move_plan
from src.board_detector import detect_board_state
from src.chess_engine import choose_move


def make_plan(task, scene, move=None):
    if task == "cup":
        return make_cup_pick_drop_plan(scene)

    if task == "chess":
        if move is None:
            board = detect_board_state()
            move = choose_move(board).uci()

        print(f"Chess move: {move}")
        return make_chess_move_plan(move, scene)

    raise ValueError(f"Unknown task: {task}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["cup", "chess"], required=True)
    parser.add_argument("--backend", choices=["mock", "real"], default="mock")
    parser.add_argument("--interface", default="eth0")
    parser.add_argument("--move", default=None, help="Chess move like e2e4")
    args = parser.parse_args()

    scene = load_config("configs/scene.yaml")["scene"]

    robot = make_g1d_controller(
        backend=args.backend,
        interface=args.interface,
    )

    commands = make_plan(args.task, scene, move=args.move)
    execute_commands(robot, commands)

    print("Task complete")


if __name__ == "__main__":
    main()
