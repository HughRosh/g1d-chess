#!/usr/bin/env python3

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class JointTrajectory:
    positions: np.ndarray
    dt: float

    @property
    def steps(self) -> int:
        return self.positions.shape[0]

    @property
    def dof(self) -> int:
        return self.positions.shape[1]


def linear_joint_trajectory(
    q_start: np.ndarray,
    q_goal: np.ndarray,
    duration: float,
    dt: float,
) -> JointTrajectory:
    if duration <= 0:
        raise ValueError("duration must be positive")

    if dt <= 0:
        raise ValueError("dt must be positive")

    q_start = np.asarray(q_start, dtype=float)
    q_goal = np.asarray(q_goal, dtype=float)

    if q_start.shape != q_goal.shape:
        raise ValueError("q_start and q_goal must have the same shape")

    steps = max(2, int(round(duration / dt)) + 1)
    alpha = np.linspace(0.0, 1.0, steps)

    positions = q_start[None, :] + alpha[:, None] * (q_goal - q_start)[None, :]

    return JointTrajectory(
        positions=positions,
        dt=dt,
    )
