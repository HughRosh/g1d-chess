#!/usr/bin/env python3

"""
Maps Pinocchio full-body q vectors to the 14-joint dual-arm
controller vector used by the G1-D hardware controller.
"""


LEFT_ARM_PIN_JOINTS = [
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
]

RIGHT_ARM_PIN_JOINTS = [
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
]


def pin_q_to_dual_arm_q(model, q):
    result = []

    for joint_name in LEFT_ARM_PIN_JOINTS + RIGHT_ARM_PIN_JOINTS:
        joint_id = model.getJointId(joint_name)
        q_index = model.idx_qs[joint_id]
        result.append(float(q[q_index]))

    return result
