#!/usr/bin/env python3

from dataclasses import dataclass
import cv2
import numpy as np


@dataclass(frozen=True)
class DetectedMarker:
    marker_id: int
    corners: np.ndarray


@dataclass(frozen=True)
class ArucoDetectionResult:
    markers: list[DetectedMarker]

    @property
    def count(self) -> int:
        return len(self.markers)

    def ids(self) -> list[int]:
        return [marker.marker_id for marker in self.markers]


class ArucoDetector:
    def __init__(self, dictionary_name: str = "DICT_4X4_50"):
        if not hasattr(cv2, "aruco"):
            raise RuntimeError("OpenCV aruco module is not available")

        dictionary_id = getattr(cv2.aruco, dictionary_name)

        self.dictionary = cv2.aruco.getPredefinedDictionary(dictionary_id)
        self.parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(
            self.dictionary,
            self.parameters,
        )

    def detect(self, image: np.ndarray) -> ArucoDetectionResult:
        corners, ids, _ = self.detector.detectMarkers(image)

        markers: list[DetectedMarker] = []

        if ids is None:
            return ArucoDetectionResult(markers=[])

        for marker_id, marker_corners in zip(ids.flatten(), corners):
            markers.append(
                DetectedMarker(
                    marker_id=int(marker_id),
                    corners=marker_corners,
                )
            )

        return ArucoDetectionResult(markers=markers)
