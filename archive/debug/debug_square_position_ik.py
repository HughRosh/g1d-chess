#!/usr/bin/env python3

import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from planning.chess_plan import square_to_xyz
from robot.kinematics.pinocchio_solver import G1DKinematics


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    kin = G1DKinematics()

    print("Square Position-Only IK Debug")
    print("=============================")

    for sq in ["e2", "e4", "e7", "e5", "c6", "b5"]:
        x, y, z = square_to_xyz(sq, scene)
        target = np.array([x, y, z + 0.12])

        q, ok, iters, err = kin.solve_position_ik(target)
        fk = kin.forward_kinematics(q)

        fk_xyz = np.array(fk["position_xyz"])
        xyz_error = np.linalg.norm(fk_xyz - target)

        print()
        print("Square:", sq)
        print("Target XYZ:", target.tolist())
        print("FK XYZ:    ", fk_xyz.tolist())
        print("IK ok:", ok)
        print("IK iters:", iters)
        print("XYZ error:", xyz_error)


if __name__ == "__main__":
    main()
