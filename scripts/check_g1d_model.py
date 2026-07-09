#!/usr/bin/env python3

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from robot.model.joint_indices import G1D_NUM_MOTOR, VALID_FOR_G1D, INVALID_FOR_G1D, JOINT_INDEX_TO_NAME
from robot.model.joint_groups import WAIST, LEFT_ARM, RIGHT_ARM, UPPER_BODY
from robot.model.gains import KP, KD

print("G1-D motor slots:", G1D_NUM_MOTOR)
print("Valid G1-D motor slots:", len(VALID_FOR_G1D))
print("Invalid/unavailable G1-D motor slots:", len(INVALID_FOR_G1D))
print("Waist:", WAIST)
print("Left arm:", LEFT_ARM)
print("Right arm:", RIGHT_ARM)
print("Upper body:", UPPER_BODY)
print("Named joints:")

for index in UPPER_BODY:
    print(f"  {index}: {JOINT_INDEX_TO_NAME[index]} | kp={KP[index]} kd={KD[index]}")
