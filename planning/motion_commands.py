#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class MotionCommand:
    action: str
    target: list | None = None
    seconds: float = 1.0
    note: str = ""

    def as_dict(self):
        return {
            "action": self.action,
            "target": self.target,
            "seconds": self.seconds,
            "note": self.note,
        }


def move_xyz(x, y, z, seconds=1.0, note=""):
    return MotionCommand(
        action="move_xyz",
        target=[float(x), float(y), float(z)],
        seconds=seconds,
        note=note,
    )


def move_joint(joint_index, delta, seconds=1.0, note=""):
    return MotionCommand(
        action="move_joint",
        target=[int(joint_index), float(delta)],
        seconds=seconds,
        note=note,
    )


def open_gripper(seconds=0.5):
    return MotionCommand(action="open_gripper", seconds=seconds)


def close_gripper(seconds=0.5):
    return MotionCommand(action="close_gripper", seconds=seconds)


def home(seconds=2.0):
    return MotionCommand(action="home", seconds=seconds)
