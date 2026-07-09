#!/usr/bin/env python3

from pathlib import Path
import argparse
import cv2
import numpy as np
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from perception.camera.stereo_split import split_side_by_side_stereo


FILES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANKS = ["1", "2", "3", "4", "5", "6", "7", "8"]


def lerp(p0, p1, t):
    return (1.0 - t) * np.array(p0, dtype=float) + t * np.array(p1, dtype=float)


def bilinear(a1, h1, a8, h8, file_t, rank_t):
    bottom = lerp(a1, h1, file_t)
    top = lerp(a8, h8, file_t)
    return lerp(bottom, top, rank_t)


def square_robot_coordinate(file_i, rank_i):
    """
    Matches the reference repo style:
    x changes by rank.
    y changes by file.
    z is constant board height.
    """
    x_by_rank = {
        1: 0.578125,
        2: 0.534375,
        3: 0.490625,
        4: 0.446875,
        5: 0.403125,
        6: 0.359375,
        7: 0.315625,
        8: 0.271875,
    }

    y_by_file = {
        "a": -0.13125,
        "b": -0.0875,
        "c": -0.04375,
        "d": 0.0,
        "e": 0.04375,
        "f": 0.0875,
        "g": 0.13125,
        "h": 0.175,
    }

    file_name = FILES[file_i]
    rank_num = rank_i + 1

    return x_by_rank[rank_num], y_by_file[file_name], 0.45


def draw_board_overlay(image, a1, h1, a8, h8):
    out = image.copy()

    # draw grid
    for i in range(9):
        t = i / 8.0

        p_bottom = bilinear(a1, h1, a8, h8, t, 0.0)
        p_top = bilinear(a1, h1, a8, h8, t, 1.0)
        p_left = bilinear(a1, h1, a8, h8, 0.0, t)
        p_right = bilinear(a1, h1, a8, h8, 1.0, t)

        cv2.line(out, tuple(p_bottom.astype(int)), tuple(p_top.astype(int)), (0, 255, 255), 2)
        cv2.line(out, tuple(p_left.astype(int)), tuple(p_right.astype(int)), (0, 255, 255), 2)

    # draw square centers and robot coordinates
    for rank_i, rank in enumerate(RANKS):
        for file_i, file in enumerate(FILES):
            file_t = (file_i + 0.5) / 8.0
            rank_t = (rank_i + 0.5) / 8.0

            p = bilinear(a1, h1, a8, h8, file_t, rank_t)
            px, py = int(p[0]), int(p[1])

            x, y, z = square_robot_coordinate(file_i, rank_i)
            square = f"{file}{rank}"

            cv2.circle(out, (px, py), 5, (0, 0, 255), -1)

            label = f"{square}"
            coord = f"x={x:.3f} y={y:.3f}"

            cv2.putText(out, label, (px - 12, py - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
            cv2.putText(out, coord, (px - 42, py + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (255, 255, 255), 1)

    # draw corner labels
    for name, point in [("a1", a1), ("h1", h1), ("a8", a8), ("h8", h8)]:
        px, py = int(point[0]), int(point[1])
        cv2.circle(out, (px, py), 8, (255, 0, 0), -1)
        cv2.putText(out, name, (px + 8, py - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    return out


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--image", default="head_frame.jpg")
    parser.add_argument("--side", choices=["left", "right", "full"], default="right")

    # These are approximate for your current right-head image.
    # Adjust them until the yellow grid sits exactly on the chessboard.
    parser.add_argument("--a1", nargs=2, type=float, default=[355, 515])
    parser.add_argument("--h1", nargs=2, type=float, default=[840, 505])
    parser.add_argument("--a8", nargs=2, type=float, default=[360, 255])
    parser.add_argument("--h8", nargs=2, type=float, default=[805, 245])

    parser.add_argument("--out", default="logs/robot_coordinate_overlay.jpg")

    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Missing {image_path}")

    frame = cv2.imread(str(image_path))

    if args.side == "left":
        left, right = split_side_by_side_stereo(frame)
        view = left
    elif args.side == "right":
        left, right = split_side_by_side_stereo(frame)
        view = right
    else:
        view = frame

    a1 = np.array(args.a1, dtype=float)
    h1 = np.array(args.h1, dtype=float)
    a8 = np.array(args.a8, dtype=float)
    h8 = np.array(args.h8, dtype=float)

    overlay = draw_board_overlay(view, a1, h1, a8, h8)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), overlay)

    print("Saved:", out_path)
    print("Open it with:")
    print(f"open {out_path}")


if __name__ == "__main__":
    main()
