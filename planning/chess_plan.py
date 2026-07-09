#!/usr/bin/env python3

from planning.motion_commands import (
    move_xyz,
    open_gripper,
    close_gripper,
)


def square_to_xyz(square, scene):
    board = scene["board"]
    table = scene["table"]

    files = "abcdefgh"
    ranks = "12345678"

    file_i = files.index(square[0])
    rank_i = ranks.index(square[1])

    square_size = board["size_m"] / 8.0

    # Board rotated 90 degrees so the robot plays from the side.
    # Files now run along robot Y; ranks run along robot X.
    x = board["x_m"] + (rank_i - 3.5) * square_size
    y = board["y_m"] + (file_i - 3.5) * square_size
    z = table["height_m"] + board["thickness_m"]

    return x, y, z


def make_chess_move_plan(move_uci, scene):
    from_square = move_uci[:2]
    to_square = move_uci[2:4]

    fx, fy, fz = square_to_xyz(from_square, scene)
    tx, ty, tz = square_to_xyz(to_square, scene)

    hover_offset = 0.36
    grasp_offset = 0.22

    return [
        move_xyz(fx, fy, fz + hover_offset, note=f"hover above {from_square}"),
        open_gripper(),
        move_xyz(fx, fy, fz + grasp_offset, note=f"descend to {from_square}"),
        close_gripper(),
        move_xyz(fx, fy, fz + hover_offset, note=f"lift from {from_square}"),
        move_xyz(tx, ty, tz + hover_offset, note=f"move above {to_square}"),
        move_xyz(tx, ty, tz + grasp_offset, note=f"place on {to_square}"),
        open_gripper(),
        move_xyz(tx, ty, tz + hover_offset, note=f"retreat from {to_square}"),
    ]
