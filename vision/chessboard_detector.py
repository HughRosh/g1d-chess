#!/usr/bin/env python3

import cv2
import numpy as np


class ChessboardDetector:
    def __init__(self, inner_corners=(7, 7), output_size=800):
        self.inner_corners = inner_corners
        self.output_size = output_size

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        found, corners = cv2.findChessboardCorners(
            gray,
            self.inner_corners,
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE,
        )

        debug = frame.copy()

        if not found:
            return {
                "found": False,
                "debug": debug,
                "warped": None,
                "occupancy": None,
            }

        corners = cv2.cornerSubPix(
            gray,
            corners,
            (11, 11),
            (-1, -1),
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001),
        )

        cv2.drawChessboardCorners(debug, self.inner_corners, corners, found)

        pts = corners.reshape(-1, 2)

        top_left = pts[0]
        top_right = pts[6]
        bottom_left = pts[42]
        bottom_right = pts[48]

        src = np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)
        dst = np.array(
            [
                [0, 0],
                [self.output_size, 0],
                [self.output_size, self.output_size],
                [0, self.output_size],
            ],
            dtype=np.float32,
        )

        H = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(frame, H, (self.output_size, self.output_size))

        occupancy = self.estimate_occupancy(warped)

        return {
            "found": True,
            "debug": debug,
            "warped": warped,
            "occupancy": occupancy,
        }

    def estimate_occupancy(self, warped):
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        square = self.output_size // 8
        occ = []

        for r in range(8):
            row = []
            for c in range(8):
                x0 = c * square
                y0 = r * square
                crop = edges[
                    y0 + square // 4 : y0 + 3 * square // 4,
                    x0 + square // 4 : x0 + 3 * square // 4,
                ]
                score = float(np.mean(crop))
                row.append(score > 12.0)
            occ.append(row)

        return occ
