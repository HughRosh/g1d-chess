from dataclasses import dataclass
from typing import Tuple


@dataclass
class BoardMapping:
    """
    Maps chess squares to robot/world XYZ coordinates.

    origin_xyz should be the center of a1.
    file_axis points from a-file toward h-file.
    rank_axis points from rank 1 toward rank 8.
    """
    origin_xyz: Tuple[float, float, float] = (0.40, -0.175, 0.75)
    square_size: float = 0.05

    def square_to_xyz(self, square: str):
        if len(square) != 2:
            raise ValueError(f"Invalid square: {square}")

        file_char = square[0].lower()
        rank_char = square[1]

        if file_char < "a" or file_char > "h" or rank_char < "1" or rank_char > "8":
            raise ValueError(f"Invalid square: {square}")

        file_idx = ord(file_char) - ord("a")
        rank_idx = int(rank_char) - 1

        x0, y0, z0 = self.origin_xyz
        x = x0 + file_idx * self.square_size
        y = y0 + rank_idx * self.square_size
        z = z0

        return [x, y, z]
