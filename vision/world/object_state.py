#!/usr/bin/env python3

from dataclasses import dataclass
from planning.kinematics import TargetPose


@dataclass
class ObjectState:
    object_id: str
    label: str
    pose: TargetPose
    confidence: float = 1.0
