#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from hardware.g1d.factory import make_g1d_controller
from planning.chess_plan import make_chess_move_plan
from planning.executor import execute_commands


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    robot = make_g1d_controller("mock")

    commands = make_chess_move_plan("e2e4", scene)

    execute_commands(
        robot,
        commands,
        use_ik=True,
    )


if __name__ == "__main__":
    main()
