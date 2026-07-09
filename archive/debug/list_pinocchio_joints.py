#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from robot.kinematics.pinocchio_solver import G1DKinematics

kin = G1DKinematics()

print()
print("Joint List")
print("==========")

for i, joint in enumerate(kin.model.names):
    print(f"{i:2d}  {joint}")
