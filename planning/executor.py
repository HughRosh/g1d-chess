#!/usr/bin/env python3

import time

from robot.kinematics.pinocchio_solver import G1DKinematics
from robot.kinematics.controller_mapping import pin_q_to_dual_arm_q


def execute_commands(robot, commands, use_ik=False):
    kin = G1DKinematics() if use_ik else None

    for i, cmd in enumerate(commands, start=1):
        print(f"[Command {i}] {cmd.as_dict()}")

        if cmd.action == "move_joint":
            joint_index, delta = cmd.target
            robot.move_joint(joint_index, delta, seconds=cmd.seconds)

        elif cmd.action == "move_pose":
            if not use_ik:
                print("[SKIP] move_pose requires IK. Re-run with use_ik=True.")
                continue

            q, ok, iters, err = kin.solve_pose_ik(cmd.target)

            print(f"IK ok={ok}, iters={iters}, err={err}")

            if not ok:
                print("[SKIP] IK failed")
                continue

            arm_q = pin_q_to_dual_arm_q(kin.model, q)
            robot.move_arm(arm_q, seconds=cmd.seconds)

        elif cmd.action == "open_gripper":
            robot.open_gripper()
            time.sleep(cmd.seconds)

        elif cmd.action == "close_gripper":
            robot.close_gripper()
            time.sleep(cmd.seconds)

        elif cmd.action == "home":
            robot.home()

        else:
            raise ValueError(f"Unknown command action: {cmd.action}")
