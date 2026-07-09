#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from robot.kinematics.pinocchio_solver import G1DKinematics

kin = G1DKinematics()

print()
print("Joint q-index mapping")
print("=====================")

for joint_id, name in enumerate(kin.model.names):
    if joint_id == 0:
        continue

    q_index = kin.model.idx_qs[joint_id]
    v_index = kin.model.idx_vs[joint_id]
    nq = kin.model.nqs[joint_id]
    nv = kin.model.nvs[joint_id]

    print(f"{joint_id:2d}  {name:32s} q={q_index:2d} v={v_index:2d} nq={nq} nv={nv}")
