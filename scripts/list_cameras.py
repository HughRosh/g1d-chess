#!/usr/bin/env python3

import cv2


def main():
    print("Scanning camera indices 0-9...")

    for i in range(10):
        cap = cv2.VideoCapture(i)
        ok = cap.isOpened()

        if ok:
            ret, _ = cap.read()
            print(f"Camera {i}: opened, read={ret}")
        else:
            print(f"Camera {i}: not available")

        cap.release()


if __name__ == "__main__":
    main()
