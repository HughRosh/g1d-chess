#!/usr/bin/env python3

import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import mujoco
import mujoco.viewer
import numpy as np

from src.utils import load_config
from planning.chess_plan import make_chess_move_plan
from robot.kinematics.pinocchio_solver import G1DKinematics

MODEL_PATH = "simulation/urdf/g1d_chess_static_scene.urdf"


def main():
    move = "e2e4"
    scene = load_config("configs/scene.yaml")["scene"]
    commands = make_chess_move_plan(move, scene)

    kin = G1DKinematics()
    q_list = []

    for cmd in commands:
        print(cmd.as_dict())

        if cmd.action == "move_pose":
            q, ok, iters, err = kin.solve_pose_ik(cmd.target)
            print("IK:", ok, "err:", err)

            if ok:
                q_list.append(q)

    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    print("Opening MuJoCo playback for chess move", move)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            for q in q_list:
                n = min(len(data.qpos), len(q))
                data.qpos[:n] = q[:n]

                for _ in range(80):
                    mujoco.mj_forward(model, data)
                    viewer.sync()
                    time.sleep(0.01)

            break

        while viewer.is_running():
            viewer.sync()
            time.sleep(0.02)


if __name__ == "__main__":
    main()
