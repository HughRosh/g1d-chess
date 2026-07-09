#!/usr/bin/env python3

from pathlib import Path
import sys
import cv2
import time

sys.path.append(str(Path(__file__).resolve().parents[1]))

from vision.camera import Camera


def main():
    cam = Camera(index=0)

    for _ in range(30):
        frame = cam.read()
        time.sleep(0.03)

    cam.release()

    # Less aggressive correction: avoid blowing out the board
    corrected = cv2.convertScaleAbs(frame, alpha=0.75, beta=-25)

    cv2.imwrite("board_capture_raw.jpg", frame)
    cv2.imwrite("board_capture_corrected.jpg", corrected)

    print("Saved board_capture_raw.jpg")
    print("Saved board_capture_corrected.jpg")


if __name__ == "__main__":
    main()
