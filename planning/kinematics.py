#!/usr/bin/env python3

"""
Kinematics utilities.

This module defines the Cartesian pose representation used
throughout the project.

All end-effector targets are represented as:

    Position (x, y, z)
    Quaternion (x, y, z, w)

No Euler angles are stored internally.

The planner should never command joints directly.
"""

from dataclasses import dataclass
import math


@dataclass
class TargetPose:

    position_xyz: list
    orientation_xyzw: list

    def as_dict(self):
        return {
            "position_xyz": self.position_xyz,
            "orientation_xyzw": self.orientation_xyzw,
        }


def quaternion_from_yaw(yaw):
    half = yaw * 0.5

    return [
        0.0,
        0.0,
        math.sin(half),
        math.cos(half),
    ]


def quaternion_multiply(q1, q2):
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2

    return [
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
    ]


def quaternion_from_rpy(roll, pitch, yaw):
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)

    return [
        sr*cp*cy - cr*sp*sy,
        cr*sp*cy + sr*cp*sy,
        cr*cp*sy - sr*sp*cy,
        cr*cp*cy + sr*sp*sy,
    ]


def make_top_down_pose(x, y, z, yaw=0.0):
    """
    Create a pose whose tool Z-axis is normal to the table.

    For now this assumes a top-down grasp with only yaw rotation.
    """

    # Board-level yaw around vertical
    yaw_q = quaternion_from_yaw(yaw)

    # Tool alignment offset:
    # Rotate the gripper frame so the tool approaches normal to the board.
    # This may need tuning depending on the Dex1.1 URDF frame convention.
    tool_down_q = quaternion_from_rpy(0.0, math.pi, 0.0)

    q = quaternion_multiply(yaw_q, tool_down_q)

    return TargetPose(
        position_xyz=[float(x), float(y), float(z)],
        orientation_xyzw=q,
    )


def placeholder_ik(target_pose):
    """
    Placeholder inverse kinematics.

    Future versions will convert the target pose into
    the 14 arm joint values used by the controller.
    """

    return [0.0] * 14
