#!/usr/bin/env python3

import sys
from pathlib import Path
import cv2

sys.path.append(str(Path(__file__).resolve().parents[1]))

from vision.camera import Camera
from vision.chessboard_detector import ChessboardDetector


def main():
    cam = Camera(index=0)
    frame = cam.read()
    cam.release()

    detector = ChessboardDetector()
    result = detector.detect(frame)

    cv2.imwrite("chess_vision_debug.jpg", result["debug"])

    if result["warped"] is not None:
        cv2.imwrite("chess_vision_warped.jpg", result["warped"])

    print("Board found:", result["found"])

    if result["occupancy"] is not None:
        print("Occupancy estimate:")
        for row in result["occupancy"]:
            print(" ".join("X" if x else "." for x in row))

    print("Saved chess_vision_debug.jpg")
    print("Saved chess_vision_warped.jpg if board was found")


if __name__ == "__main__":
    main()
