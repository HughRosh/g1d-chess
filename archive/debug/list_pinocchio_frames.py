#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from robot.kinematics.pinocchio_solver import G1DKinematics

kin = G1DKinematics()

print()
print("Frames:")
for i, frame in enumerate(kin.model.frames):
    name = frame.name
    if "right" in name.lower() or "dex" in name.lower() or "wrist" in name.lower():
        print(i, name)
