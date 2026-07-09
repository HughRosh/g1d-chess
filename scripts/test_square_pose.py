#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.utils import load_config
from chessbot.square_pose import square_pose

scene = load_config("configs/scene.yaml")["scene"]

for square in ["a1", "e2", "e4", "h8"]:
    pose = square_pose(square, scene)
    print(square, pose.as_dict())
