#!/usr/bin/env python3

from dataclasses import dataclass
import math


FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Vector3D:
    x: float
    y: float
    z: float

    def normalized(self) -> "Vector3D":
        mag = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return Vector3D(self.x / mag, self.y / mag, self.z / mag)

    def scaled(self, scale: float) -> "Vector3D":
        return Vector3D(self.x * scale, self.y * scale, self.z * scale)


def add_point_vector(point: Point3D, vector: Vector3D) -> Point3D:
    return Point3D(
        x=point.x + vector.x,
        y=point.y + vector.y,
        z=point.z + vector.z,
    )


@dataclass(frozen=True)
class ChessBoardGeometry:
    origin_a1: Point3D
    file_direction: Vector3D
    rank_direction: Vector3D
    square_size: float
    approach_height: float = 0.10
    pick_height: float = 0.02

    def square_center(self, square: str) -> Point3D:
        if len(square) != 2:
            raise ValueError(f"Invalid square name: {square}")

        file_char = square[0].lower()
        rank_char = square[1]

        if file_char not in FILES:
            raise ValueError(f"Invalid file: {file_char}")

        if rank_char not in RANKS:
            raise ValueError(f"Invalid rank: {rank_char}")

        file_index = FILES.index(file_char)
        rank_index = RANKS.index(rank_char)

        file_step = self.file_direction.normalized().scaled(file_index * self.square_size)
        rank_step = self.rank_direction.normalized().scaled(rank_index * self.square_size)

        p = add_point_vector(self.origin_a1, file_step)
        p = add_point_vector(p, rank_step)

        return p

    def approach_point(self, square: str) -> Point3D:
        center = self.square_center(square)
        return Point3D(
            x=center.x,
            y=center.y,
            z=center.z + self.approach_height,
        )

    def pick_point(self, square: str) -> Point3D:
        center = self.square_center(square)
        return Point3D(
            x=center.x,
            y=center.y,
            z=center.z + self.pick_height,
        )


def create_axis_aligned_board(
    origin_a1: Point3D,
    square_size: float,
    approach_height: float = 0.10,
    pick_height: float = 0.02,
) -> ChessBoardGeometry:
    return ChessBoardGeometry(
        origin_a1=origin_a1,
        file_direction=Vector3D(1.0, 0.0, 0.0),
        rank_direction=Vector3D(0.0, 1.0, 0.0),
        square_size=square_size,
        approach_height=approach_height,
        pick_height=pick_height,
    )
