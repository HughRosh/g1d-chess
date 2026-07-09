#!/usr/bin/env python3

from dataclasses import dataclass, field

from robot.state.joint_state import JointState
from robot.state.imu_state import IMUState


@dataclass
class RobotState:
    joints: JointState = field(default_factory=JointState)
    imu: IMUState = field(default_factory=IMUState)
    mode_machine: int = 0
