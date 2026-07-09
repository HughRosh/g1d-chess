#!/usr/bin/env python3

from planning.motion_commands import (
    move_xyz,
    open_gripper,
    close_gripper,
)


def make_cup_pick_drop_plan(scene):
    table = scene["table"]
    cup = scene["cup"]

    cup_x = cup["x_m"]
    cup_y = cup["y_m"]
    table_z = table["height_m"]
    cup_h = cup["height_m"]

    hover_z = table_z + cup_h + 0.15
    grasp_z = table_z + cup_h * 0.50

    drop_x = cup_x
    drop_y = cup_y + 0.35
    drop_z = table_z + cup_h + 0.20

    return [
        move_xyz(cup_x, cup_y, hover_z, note="hover above cup"),
        open_gripper(),
        move_xyz(cup_x, cup_y, grasp_z, note="descend to cup"),
        close_gripper(),
        move_xyz(cup_x, cup_y, hover_z, note="lift cup"),
        move_xyz(drop_x, drop_y, drop_z, note="move to drop zone"),
        open_gripper(),
        move_xyz(drop_x, drop_y, hover_z, note="retreat"),
    ]
