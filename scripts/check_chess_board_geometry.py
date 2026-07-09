#!/usr/bin/env python3

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from apps.chess.board_geometry import Point3D, Vector3D, ChessBoardGeometry
from apps.chess.move import ChessMove
from apps.chess.task_builder import build_pick_place_task

board = ChessBoardGeometry(
    origin_a1=Point3D(x=0.30, y=-0.20, z=0.00),
    file_direction=Vector3D(x=0.866, y=0.500, z=0.0),
    rank_direction=Vector3D(x=-0.500, y=0.866, z=0.0),
    square_size=0.05,
)

move = ChessMove.from_uci("e2e4")
task = build_pick_place_task(move, board)

print("Move:", move)
print("Source approach:", task.source_approach)
print("Source pick:", task.source_pick)
print("Target approach:", task.target_approach)
print("Target place:", task.target_place)
