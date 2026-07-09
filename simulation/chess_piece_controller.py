from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from simulation.engine import MujocoEngine


BOARD_CENTER_X = 0.274
BOARD_CENTER_Y = 0.0
SQUARE_SIZE = 0.05
PIECE_Z = 0.7895


def square_xyz(square: str, z: float = PIECE_Z) -> tuple[float, float, float]:
    file_char = square[0].lower()
    rank = int(square[1])

    file_idx = ord(file_char) - ord("a")
    rank_idx = rank - 1

    x = BOARD_CENTER_X + (-0.175 + file_idx * SQUARE_SIZE)
    y = BOARD_CENTER_Y + (-0.175 + rank_idx * SQUARE_SIZE)
    return (x, y, z)


@dataclass
class PieceController:
    engine: MujocoEngine
    carried_piece_joint: str | None = None
    carry_offset: np.ndarray | None = None

    def set_piece_square(self, piece_square: str, target_square: str) -> None:
        self.engine.set_free_joint_pose(
            f"piece_{piece_square}_free",
            square_xyz(target_square),
        )

    def attach(self, piece_square: str, gripper_joint: str) -> None:
        piece_joint = f"piece_{piece_square}_free"
        piece_xyz = self.engine.get_free_joint_xyz(piece_joint)
        gripper_xyz = self.engine.get_free_joint_xyz(gripper_joint)

        self.carried_piece_joint = piece_joint
        self.carry_offset = piece_xyz - gripper_xyz

    def update_carried_piece(self, gripper_joint: str) -> None:
        if self.carried_piece_joint is None or self.carry_offset is None:
            return

        gripper_xyz = self.engine.get_free_joint_xyz(gripper_joint)
        piece_xyz = gripper_xyz + self.carry_offset
        self.engine.set_free_joint_pose(self.carried_piece_joint, tuple(piece_xyz))

    def release_at(self, target_square: str) -> None:
        if self.carried_piece_joint is None:
            return

        self.engine.set_free_joint_pose(
            self.carried_piece_joint,
            square_xyz(target_square),
        )
        self.carried_piece_joint = None
        self.carry_offset = None
