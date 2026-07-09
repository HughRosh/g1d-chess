#!/usr/bin/env python3

from robot.state.robot_state import RobotState

state = RobotState()

print(state)
print("Joint count:", len(state.joints.q))
