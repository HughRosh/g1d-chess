#!/usr/bin/env python3

import time


def execute_commands(robot, commands):
    for i, cmd in enumerate(commands, start=1):
        print(f"[Command {i}] {cmd.as_dict()}")

        if cmd.action == "move_joint":
            joint_index, delta = cmd.target
            robot.move_joint(joint_index, delta, seconds=cmd.seconds)

        elif cmd.action == "open_gripper":
            robot.open_gripper()
            time.sleep(cmd.seconds)

        elif cmd.action == "close_gripper":
            robot.close_gripper()
            time.sleep(cmd.seconds)

        elif cmd.action == "home":
            robot.home()

        elif cmd.action == "move_xyz":
            print("[SKIP] move_xyz requires IK, not implemented yet")

        else:
            raise ValueError(f"Unknown command action: {cmd.action}")
