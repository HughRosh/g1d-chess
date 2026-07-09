#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from robot.model.g1d_model import *

print("Right arm:")
for joint in RIGHT_ARM:
    print(" ", joint)

print()

print("Left arm:")
for joint in LEFT_ARM:
    print(" ", joint)
