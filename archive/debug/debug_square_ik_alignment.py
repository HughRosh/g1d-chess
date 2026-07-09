#!/usr/bin/env python3

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from planning.kinematics import make_top_down_pose
from planning.chess_plan import square_to_xyz
from robot.kinematics.pinocchio_solver import G1DKinematics


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    kin = G1DKinematics()

    print("Square IK Alignment Debug")
    print("=========================")

    for sq in ["e2", "e4", "e7", "e5", "c6", "b5"]:
        x, y, z = square_to_xyz(sq, scene)

        target = make_top_down_pose(
            x=x,
            y=y,
            z=z + 0.12,
            yaw=0.0,
        )

        q, ok, iters, err = kin.solve_pose_ik(target)
        fk = kin.forward_kinematics(q)

        fk_xyz = np.array(fk["position_xyz"])
        target_xyz = np.array(target.position_xyz)
        xyz_error = np.linalg.norm(fk_xyz - target_xyz)

        print()
        print("Square:", sq)
        print("Target XYZ:", target_xyz.tolist())
        print("FK XYZ:    ", fk_xyz.tolist())
        print("IK ok:", ok)
        print("IK iters:", iters)
        print("IK SE3 err:", err)
        print("XYZ error:", xyz_error)


if __name__ == "__main__":
    main()
