#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from planning.kinematics import make_top_down_pose
from robot.kinematics.pinocchio_solver import G1DKinematics
from robot.kinematics.controller_mapping import pin_q_to_dual_arm_q

kin = G1DKinematics()

start = kin.forward_kinematics()
target = make_top_down_pose(
    start["position_xyz"][0] + 0.03,
    start["position_xyz"][1],
    start["position_xyz"][2],
)

q, ok, iters, err = kin.solve_pose_ik(target)

arm_q = pin_q_to_dual_arm_q(kin.model, q)

print("IK ok:", ok)
print("IK error:", err)
print("Controller arm q:")
print(arm_q)
print("Length:", len(arm_q))
