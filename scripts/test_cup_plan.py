#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from hardware.g1d.factory import make_g1d_controller
from planning.cup_plan import make_cup_pick_drop_plan
from planning.executor import execute_commands


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    robot = make_g1d_controller("mock")

    commands = make_cup_pick_drop_plan(scene)
    execute_commands(robot, commands)


if __name__ == "__main__":
    main()
