from dataclasses import dataclass
from typing import List, Optional

from ultralytics import YOLO


@dataclass
class Detection:
    label: str
    confidence: float
    xyxy: list


class YOLOChessDetector:
    def __init__(self, model_path: str = "yolo11n.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path: str, conf: float = 0.25) -> List[Detection]:
        results = self.model(image_path, conf=conf)
        detections = []

        for result in results:
            names = result.names

            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = names[cls_id]
                confidence = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()

                detections.append(
                    Detection(
                        label=label,
                        confidence=confidence,
                        xyxy=xyxy,
                    )
                )

        return detections

    def best_board_candidate(self, image_path: str) -> Optional[Detection]:
        detections = self.detect(image_path)

        # Temporary fallback: YOLO base model may not know "chessboard".
        # This lets us verify the detector pipeline works before training custom weights.
        candidates = [
            d for d in detections
            if d.label.lower() in {"chessboard", "board", "sports ball", "book", "laptop"}
        ]

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda d: (d.xyxy[2] - d.xyxy[0]) * (d.xyxy[3] - d.xyxy[1])
        )
