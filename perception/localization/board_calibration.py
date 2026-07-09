#!/usr/bin/env python3

from dataclasses import dataclass

from apps.chess.board_geometry import Point3D, Vector3D, ChessBoardGeometry


@dataclass(frozen=True)
class BoardCalibration:
    origin_a1: Point3D
    file_direction: Vector3D
    rank_direction: Vector3D
    square_size: float
    approach_height: float = 0.10
    pick_height: float = 0.02

    def to_geometry(self) -> ChessBoardGeometry:
        return ChessBoardGeometry(
            origin_a1=self.origin_a1,
            file_direction=self.file_direction,
            rank_direction=self.rank_direction,
            square_size=self.square_size,
            approach_height=self.approach_height,
            pick_height=self.pick_height,
        )


def default_manual_board_calibration() -> BoardCalibration:
    return BoardCalibration(
        origin_a1=Point3D(x=0.30, y=-0.20, z=0.00),
        file_direction=Vector3D(x=1.0, y=0.0, z=0.0),
        rank_direction=Vector3D(x=0.0, y=1.0, z=0.0),
        square_size=0.05,
    )
