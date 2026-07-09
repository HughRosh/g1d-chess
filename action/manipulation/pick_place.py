#!/usr/bin/env python3

from planning.motion_commands import (
    move_xyz,
    open_gripper,
    close_gripper,
)


def make_pick_place_commands(pick_pose, place_pose):
    return [
        move_xyz(*pick_pose.position_xyz, note="hover above pick"),
        open_gripper(),
        move_xyz(*pick_pose.position_xyz, note="descend to pick"),
        close_gripper(),
        move_xyz(*pick_pose.position_xyz, note="lift object"),
        move_xyz(*place_pose.position_xyz, note="move to place"),
        open_gripper(),
        move_xyz(*place_pose.position_xyz, note="retreat"),
    ]
