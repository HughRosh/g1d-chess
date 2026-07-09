#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from planning.kinematics import make_top_down_pose
from robot.kinematics.pinocchio_solver import G1DKinematics

kin = G1DKinematics()

start = kin.forward_kinematics()
print("Start FK:")
print(start["position_xyz"])

target = make_top_down_pose(
    start["position_xyz"][0] + 0.03,
    start["position_xyz"][1],
    start["position_xyz"][2],
    yaw=0.0,
)

q, ok, iters, err = kin.solve_pose_ik(target)

print()
print("Pose IK result")
print("ok:", ok)
print("iters:", iters)
print("error:", err)

after = kin.forward_kinematics(q)

print()
print("After FK:")
print(after["position_xyz"])
print("Target:")
print(target.as_dict())
