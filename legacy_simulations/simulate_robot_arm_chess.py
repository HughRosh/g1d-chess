#!/usr/bin/env python3

import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils import load_config
from planning.chess_plan import make_chess_move_plan
from robot.kinematics.pinocchio_solver import G1DKinematics
from robot.kinematics.controller_mapping import pin_q_to_dual_arm_q

MODEL_PATH = "simulation/urdf/g1d_chess_static_scene.urdf"


def interp(q0, q1, steps=80):
    q0 = np.asarray(q0, dtype=float)
    q1 = np.asarray(q1, dtype=float)
    for a in np.linspace(0, 1, steps):
        yield (1 - a) * q0 + a * q1


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    commands = make_chess_move_plan("e2e4", scene)

    kin = G1DKinematics()

    robot_arm_waypoints = []
    for cmd in commands:
        if cmd.action != "move_pose":
            print(cmd.as_dict())
            continue

        q, ok, iters, err = kin.solve_pose_ik(cmd.target)
        print(cmd.note, "IK:", ok, "err:", err)

        if ok:
            arm_q = pin_q_to_dual_arm_q(kin.model, q)
            robot_arm_waypoints.append(arm_q)

    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    q_current = np.zeros(14)

    print("Animating actual robot arm for e2e4. Close viewer to exit.")

    with mujoco.viewer.launch_passive(model, data) as viewer:
        for q_target in robot_arm_waypoints:
            for q in interp(q_current, q_target):
                n = min(len(data.qpos), len(q))
                data.qpos[:n] = q[:n]

                mujoco.mj_forward(model, data)
                viewer.sync()
                time.sleep(0.015)

            q_current = np.asarray(q_target)

        while viewer.is_running():
            viewer.sync()
            time.sleep(0.03)


if __name__ == "__main__":
    main()
