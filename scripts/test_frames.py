#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.frames import *

print()
print("Coordinate Frames")
print("-----------------")
print(WORLD)
print(ROBOT_BASE)
print(TABLE)
print(BOARD)
