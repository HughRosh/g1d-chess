import cv2
import numpy as np


class BoardROIDetector:
    """
    Automatic board detector tuned for the real camera view.

    It ignores the room and searches only the lower-center region where the
    chessboard is expected.
    """

    def __init__(
        self,
        x_min=0.10,
        x_max=0.82,
        y_min=0.48,
        y_max=0.98,
    ):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def detect_board_corners(self, image_bgr):
        h, w = image_bgr.shape[:2]

        x0 = int(w * self.x_min)
        x1 = int(w * self.x_max)
        y0 = int(h * self.y_min)
        y1 = int(h * self.y_max)

        roi = image_bgr[y0:y1, x0:x1]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 30, 100)

        kernel = np.ones((5, 5), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
        edges = cv2.dilate(edges, kernel, iterations=1)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        best_rect = None
        best_score = -1

        for c in contours:
            area = cv2.contourArea(c)
            if area < 15000:
                continue

            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect).astype(np.float32)

            rx, ry, rw, rh = cv2.boundingRect(box.astype(np.int32))
            aspect = rw / max(rh, 1)

            if aspect < 1.2 or aspect > 4.5:
                continue

            fill = area / max(rw * rh, 1)
            if fill < 0.15:
                continue

            # Prefer large, lower, center-ish board candidates.
            cx = rx + rw / 2
            cy = ry + rh / 2
            center_score = 1.0 - abs(cx - roi.shape[1] / 2) / (roi.shape[1] / 2)
            lower_score = cy / roi.shape[0]
            score = area * (0.7 + center_score) * (0.7 + lower_score)

            if score > best_score:
                best_score = score
                best_rect = box

        if best_rect is None:
            raise RuntimeError("Could not detect chessboard in lower-center ROI")

        best_rect[:, 0] += x0
        best_rect[:, 1] += y0

        return self._order_corners(best_rect)

    def square_centers_image(self, image_bgr):
        tl, tr, br, bl = self.detect_board_corners(image_bgr)

        centers = {}
        for rank_from_top in range(8):
            for file_idx in range(8):
                u = (file_idx + 0.5) / 8.0
                v = (rank_from_top + 0.5) / 8.0

                top = tl * (1 - u) + tr * u
                bottom = bl * (1 - u) + br * u
                point = top * (1 - v) + bottom * v

                square = f"{chr(ord('a') + file_idx)}{8 - rank_from_top}"
                centers[square] = point.tolist()

        return centers

    def debug_draw(self, image_bgr):
        image = image_bgr.copy()
        h, w = image.shape[:2]

        x0 = int(w * self.x_min)
        x1 = int(w * self.x_max)
        y0 = int(h * self.y_min)
        y1 = int(h * self.y_max)

        cv2.rectangle(image, (x0, y0), (x1, y1), (255, 0, 0), 2)

        corners = self.detect_board_corners(image_bgr)
        centers = self.square_centers_image(image_bgr)

        cv2.polylines(image, [corners.astype(int)], True, (0, 255, 255), 4)

        for square, point in centers.items():
            x, y = map(int, point)
            cv2.circle(image, (x, y), 4, (0, 255, 0), -1)
            cv2.putText(
                image,
                square,
                (x + 3, y - 3),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (0, 255, 0),
                1,
            )

        return image

    def _order_corners(self, pts):
        pts = np.array(pts, dtype=np.float32)

        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1).reshape(-1)

        tl = pts[np.argmin(s)]
        br = pts[np.argmax(s)]
        tr = pts[np.argmin(diff)]
        bl = pts[np.argmax(diff)]

        return np.array([tl, tr, br, bl], dtype=np.float32)
