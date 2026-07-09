#!/usr/bin/env python3

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config

OUT = Path("simulation/mujoco/chess_piece_scene.xml")
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


def starting_pieces():
    pieces = {}
    for f in "abcdefgh":
        pieces[f"{f}2"] = "white"
        pieces[f"{f}7"] = "black"

    for sq in ["a1","h1"]:
        pieces[sq] = "white"
    for sq in ["b1","g1"]:
        pieces[sq] = "white"
    for sq in ["c1","f1"]:
        pieces[sq] = "white"
    pieces["d1"] = "white"
    pieces["e1"] = "white"

    for sq in ["a8","h8"]:
        pieces[sq] = "black"
    for sq in ["b8","g8"]:
        pieces[sq] = "black"
    for sq in ["c8","f8"]:
        pieces[sq] = "black"
    pieces["d8"] = "black"
    pieces["e8"] = "black"

    return pieces


def main():
    scene = load_config("configs/scene.yaml")["scene"]
    table = scene["table"]
    board = scene["board"]

    table_z = table["height_m"]
    board_z = table_z + board["thickness_m"] / 2.0
    piece_z = table_z + board["thickness_m"] + PIECE_HEIGHT / 2.0

    xml = f'''<mujoco model="g1d_chess_piece_scene">
  <compiler angle="radian"/>
  <option timestep="0.002"/>

  <asset>
    <material name="table_mat" rgba="0.32 0.16 0.07 1"/>
    <material name="light_square" rgba="0.85 0.68 0.42 1"/>
    <material name="dark_square" rgba="0.32 0.16 0.07 1"/>
    <material name="white_piece" rgba="0.95 0.86 0.65 1"/>
    <material name="black_piece" rgba="0.12 0.05 0.025 1"/>
  </asset>

  <worldbody>
    <light pos="0 0 3"/>

    <geom name="table" type="box"
          pos="{table['x_m']} {table['y_m']} {table_z - table['thickness_m']/2.0}"
          size="{table['size_x_m']/2.0} {table['size_y_m']/2.0} {table['thickness_m']/2.0}"
          material="table_mat"/>

    <body name="board" pos="{board['x_m']} {board['y_m']} {board_z}">
'''

    s = board["size_m"] / 8.0
    for r in range(8):
        for f in range(8):
            x = (f - 3.5) * s
            y = (r - 3.5) * s
            mat = "light_square" if (r + f) % 2 == 0 else "dark_square"
            xml += f'      <geom type="box" pos="{x} {y} 0.004" size="{s/2} {s/2} 0.004" material="{mat}"/>\n'

    xml += "    </body>\n\n"

    for sq, color in starting_pieces().items():
        x, y = square_xy(sq, scene)
        mat = "white_piece" if color == "white" else "black_piece"
        xml += f'''    <body name="piece_{sq}" pos="{x} {y} {piece_z}">
      <joint name="piece_{sq}_free" type="free"/>
      <geom type="cylinder" size="{PIECE_RADIUS} {PIECE_HEIGHT/2.0}" material="{mat}"/>
      <geom type="sphere" pos="0 0 {PIECE_HEIGHT/2.0}" size="{PIECE_RADIUS*0.8}" material="{mat}"/>
    </body>

'''

    xml += '''    <body name="gripper_marker" pos="0.25 -0.35 1.05">
      <joint name="gripper_marker_free" type="free"/>
      <geom type="sphere" size="0.025" rgba="0.1 0.4 1.0 1"/>
      <geom type="capsule" fromto="0 0 0 0 0 -0.10" size="0.01" rgba="0.1 0.4 1.0 1"/>
    </body>

  </worldbody>
</mujoco>
'''

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(xml)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
