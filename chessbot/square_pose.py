#!/usr/bin/env python3

"""
Square pose utilities.

Converts chess squares into full Cartesian target poses:
XYZ position + XYZW quaternion orientation.
"""

from chessbot.board import ChessBoardGeometry
from planning.kinematics import make_top_down_pose


def square_pose(square, scene, z_offset_m=0.15, yaw=0.0):
    board = ChessBoardGeometry(scene)
    table = scene["table"]
    board_cfg = scene["board"]

    x, y = board.square_center(square)

    z = (
        table["height_m"]
        + board_cfg["thickness_m"]
        + z_offset_m
    )

    return make_top_down_pose(
        x=x,
        y=y,
        z=z,
        yaw=yaw,
    )
