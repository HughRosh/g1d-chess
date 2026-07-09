#!/usr/bin/env python3

import numpy as np

from robot.model.joint_indices import G1D_NUM_MOTOR
from robot.model.joint_groups import LEFT_ARM, RIGHT_ARM


def make_full_body_target_from_arm_targets(
    current_q: np.ndarray,
    left_arm_target: list[float] | None = None,
    right_arm_target: list[float] | None = None,
) -> np.ndarray:
    q_goal = np.asarray(current_q, dtype=float).copy()

    if q_goal.shape[0] != G1D_NUM_MOTOR:
        raise ValueError(f"Expected current_q with {G1D_NUM_MOTOR} values")

    if left_arm_target is not None:
        if len(left_arm_target) != len(LEFT_ARM):
            raise ValueError(f"Expected {len(LEFT_ARM)} left arm target values")
        for index, value in zip(LEFT_ARM, left_arm_target):
            q_goal[index] = value

    if right_arm_target is not None:
        if len(right_arm_target) != len(RIGHT_ARM):
            raise ValueError(f"Expected {len(RIGHT_ARM)} right arm target values")
        for index, value in zip(RIGHT_ARM, right_arm_target):
            q_goal[index] = value

    return q_goal
