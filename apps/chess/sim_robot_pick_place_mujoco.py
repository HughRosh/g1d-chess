from __future__ import annotations

from pathlib import Path
import time

import mujoco
import mujoco.viewer
import numpy as np

from simulation.engine import MujocoEngine
from simulation.chess_piece_controller import PieceController, square_xyz


ROOT = Path(__file__).resolve().parents[2]
SCENE = ROOT / "simulation" / "urdf" / "g1d_chess_robot_piece_scene.urdf"

GRIPPER_BODY_1 = "right_dex1_finger_link_1"
GRIPPER_BODY_2 = "right_dex1_finger_link_2"


def midpoint(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a + b) / 2.0


class RobotSceneDiagnostic:
    def __init__(self):
        self.engine = MujocoEngine(str(SCENE))
        self.pieces = PieceController(self.engine)

        self.frame = 0
        self.carried = False
        self.released = False

    def gripper_xyz(self) -> np.ndarray:
        a = self.engine.get_body_xyz(GRIPPER_BODY_1)
        b = self.engine.get_body_xyz(GRIPPER_BODY_2)
        return midpoint(a, b)

    def tick(self) -> bool:
        self.frame += 1

        gripper = self.gripper_xyz()

        if self.frame == 1:
            print("Loaded robot + chess scene.")
            print("Real gripper midpoint:", gripper)
            print("piece_e2 start:", self.engine.get_free_joint_xyz("piece_e2_free"))

        if self.frame == 120 and not self.carried:
            print("Attaching piece_e2 to real gripper midpoint.")
            piece_xyz = self.engine.get_free_joint_xyz("piece_e2_free")
            offset = piece_xyz - gripper

            self.pieces.carried_piece_joint = "piece_e2_free"
            self.pieces.carry_offset = offset
            self.carried = True

        if self.carried and not self.released:
            piece_xyz = gripper + self.pieces.carry_offset
            self.engine.set_free_joint_pose("piece_e2_free", tuple(piece_xyz))

        if self.frame == 360 and self.carried and not self.released:
            print("Releasing piece_e2 at e4.")
            self.pieces.release_at("e4")
            print("piece_e2 final:", self.engine.get_free_joint_xyz("piece_e2_free"))
            self.released = True

        return self.frame > 520

    def run(self) -> None:
        print("Launching robot-scene diagnostic.")
        print("This uses the real robot scene and tracks right Dex1 finger bodies.")
        self.engine.launch(self.tick)
        print("Done.")


if __name__ == "__main__":
    RobotSceneDiagnostic().run()
