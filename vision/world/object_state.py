from dataclasses import dataclass

from planning.kinematics import TargetPose


@dataclass
class ObjectState:

    object_id: str

    category: str

    subtype: str

    color: str

    pose: TargetPose

    confidence: float
