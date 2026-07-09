#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from hardware.g1d.factory import make_g1d_controller
from planning.motion_commands import move_joint, open_gripper, close_gripper, home
from planning.executor import execute_commands

RIGHT_SHOULDER_PITCH = 7


def main():
    robot = make_g1d_controller("mock")

    commands = [
        move_joint(RIGHT_SHOULDER_PITCH, 0.10, seconds=1.0, note="small right arm move"),
        open_gripper(),
        close_gripper(),
        open_gripper(),
        move_joint(RIGHT_SHOULDER_PITCH, -0.10, seconds=1.0, note="return right arm"),
        home(),
    ]

    execute_commands(robot, commands)


if __name__ == "__main__":
    main()
