#!/usr/bin/env python3

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from perception.localization.board_calibration import default_manual_board_calibration
from apps.chess.move import ChessMove
from apps.chess.task_builder import build_pick_place_task

calibration = default_manual_board_calibration()
board = calibration.to_geometry()

move = ChessMove.from_uci("e2e4")
task = build_pick_place_task(move, board)

print("Calibration:", calibration)
print("Move:", move)
print("Source pick:", task.source_pick)
print("Target place:", task.target_place)
