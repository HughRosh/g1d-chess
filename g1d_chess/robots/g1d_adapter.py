from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Pose:
    xyz: List[float]
    quat: Optional[List[float]] = None


class G1DAdapter:
    """
    First-pass G1-D adapter.

    This is a safe stub: it prints intended commands instead of moving hardware.
    Later, replace _send_cartesian_command and _send_gripper_command with Unitree SDK calls.
    """

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def observe(self) -> Dict:
        return {
            "images": {},
            "state": {
                "robot": "unitree_g1d",
                "control_mode": "cartesian_eef",
            },
        }

    def move_pose(self, xyz, quat=None, arm: str = "right"):
        pose = Pose(list(xyz), quat)
        self._send_cartesian_command(arm, pose)

    def gripper(self, value: float, arm: str = "right"):
        value = max(0.0, min(1.0, float(value)))
        self._send_gripper_command(arm, value)

    def pick(self, xyz, arm: str = "right"):
        x, y, z = xyz
        self.move_pose([x, y, z + 0.10], arm=arm)
        self.move_pose([x, y, z + 0.02], arm=arm)
        self.gripper(1.0, arm=arm)
        self.move_pose([x, y, z + 0.12], arm=arm)

    def place(self, xyz, arm: str = "right"):
        x, y, z = xyz
        self.move_pose([x, y, z + 0.10], arm=arm)
        self.move_pose([x, y, z + 0.02], arm=arm)
        self.gripper(0.0, arm=arm)
        self.move_pose([x, y, z + 0.12], arm=arm)

    def _send_cartesian_command(self, arm: str, pose: Pose):
        print(f"[G1DAdapter] {arm} arm move_pose xyz={pose.xyz} quat={pose.quat}")

    def _send_gripper_command(self, arm: str, value: float):
        print(f"[G1DAdapter] {arm} gripper={value}")
