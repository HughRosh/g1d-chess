#!/usr/bin/env python3

"""
Canonical G1-D robot model.

This file defines the logical joint groups used by the rest of
the software. No other module should hardcode joint indices.
"""

RIGHT_ARM = [
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
]

LEFT_ARM = [
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
]

RIGHT_GRIPPER = [
    "right_dex1_finger_joint_1",
    "right_dex1_finger_joint_2",
]

LEFT_GRIPPER = [
    "left_dex1_finger_joint_1",
    "left_dex1_finger_joint_2",
]

ARM_GROUPS = {
    "left": LEFT_ARM,
    "right": RIGHT_ARM,
}
