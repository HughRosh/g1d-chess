#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.quaternion import *

print(identity())
print(from_yaw(0.0))
print(from_yaw(1.57))
