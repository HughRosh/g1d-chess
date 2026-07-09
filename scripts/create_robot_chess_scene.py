#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from pathlib import Path
from src.utils import load_config

BASE = Path("simulation/urdf/g1d_chess_static_scene.urdf")
OUT = Path("simulation/urdf/g1d_chess_robot_piece_scene.urdf")

PIECE_RADIUS = 0.018
PIECE_HEIGHT = 0.055


def square_xy(square, scene):
    board = scene["board"]
    files = "abcdefgh"
    ranks = "12345678"
    f = files.index(square[0])
    r = ranks.index(square[1])
    s = board["size_m"] / 8.0
    x = board["x_m"] + (f - 3.5) * s
    y = board["y_m"] + (r - 3.5) * s
    return x, y


def starting_squares():
    return (
        [f"{f}2" for f in "abcdefgh"]
        + [f"{f}7" for f in "abcdefgh"]
        + ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]
        + ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]
    )


def piece_color(square):
    return "white" if square[1] in ["1", "2"] else "black"


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    table = scene["table"]
    board = scene["board"]

    text = BASE.read_text()
    insert = ""

    parent_link = "AGV_link"

    piece_z = table["height_m"] + board["thickness_m"] + PIECE_HEIGHT / 2.0

    for sq in starting_squares():
        x, y = square_xy(sq, scene)
        color = piece_color(sq)

        rgba = "0.95 0.86 0.65 1" if color == "white" else "0.12 0.05 0.025 1"

        insert += f'''
  <link name="piece_{sq}">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="{PIECE_RADIUS}" length="{PIECE_HEIGHT}"/>
      </geometry>
      <material name="{color}_piece_{sq}">
        <color rgba="{rgba}"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="{PIECE_RADIUS}" length="{PIECE_HEIGHT}"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <mass value="0.03"/>
      <inertia ixx="0.00001" ixy="0" ixz="0" iyy="0.00001" iyz="0" izz="0.00001"/>
    </inertial>
  </link>

  <joint name="piece_{sq}_free" type="floating">
    <parent link="{parent_link}"/>
    <child link="piece_{sq}"/>
    <origin xyz="{x} {y} {piece_z}" rpy="0 0 0"/>
  </joint>
'''

    text = text.replace("</robot>", insert + "\n</robot>")
    OUT.write_text(text)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
