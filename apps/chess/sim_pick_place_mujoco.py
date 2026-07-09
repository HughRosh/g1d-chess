from __future__ import annotations

from pathlib import Path

import numpy as np

from simulation.engine import MujocoEngine
from simulation.chess_piece_controller import PieceController, square_xyz


ROOT = Path(__file__).resolve().parents[2]
SCENE = ROOT / "simulation" / "mujoco" / "g1d_chess_scene.xml"

GRIPPER_JOINT = "gripper_marker_free"


def lerp(a, b, t: float):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return tuple(a + (b - a) * t)


class PickPlaceDemo:
    def __init__(self):
        self.engine = MujocoEngine(str(SCENE))
        self.pieces = PieceController(self.engine)

        self.steps = []
        self.step_index = 0
        self.local_step = 0

        e2 = square_xyz("e2")
        e4 = square_xyz("e4")

        self.above_e2 = (e2[0], e2[1], e2[2] + 0.18)
        self.pick_e2 = (e2[0], e2[1], e2[2] + 0.055)
        self.above_e4 = (e4[0], e4[1], e4[2] + 0.18)
        self.place_e4 = (e4[0], e4[1], e4[2] + 0.055)

        self.engine.set_free_joint_pose(GRIPPER_JOINT, self.above_e2)

        self.steps = [
            ("move", self.above_e2, self.pick_e2, 180),
            ("attach", None, None, 30),
            ("move", self.pick_e2, self.above_e2, 180),
            ("move", self.above_e2, self.above_e4, 260),
            ("move", self.above_e4, self.place_e4, 180),
            ("release", None, None, 30),
            ("move", self.place_e4, self.above_e4, 180),
        ]

    def tick(self) -> bool:
        if self.step_index >= len(self.steps):
            return True

        action, start, end, duration = self.steps[self.step_index]

        if action == "move":
            t = min(1.0, self.local_step / duration)
            xyz = lerp(start, end, t)
            self.engine.set_free_joint_pose(GRIPPER_JOINT, xyz)
            self.pieces.update_carried_piece(GRIPPER_JOINT)

        elif action == "attach" and self.local_step == 0:
            self.pieces.attach("e2", GRIPPER_JOINT)

        elif action == "release" and self.local_step == 0:
            self.pieces.release_at("e4")

        self.local_step += 1

        if self.local_step >= duration:
            self.step_index += 1
            self.local_step = 0

        return False

    def run(self) -> None:
        print("Launching clean pick/place demo: e2 -> e4")
        print("This verifies piece attachment/release logic using the blue gripper marker.")
        self.engine.launch(self.tick)
        print("Done. piece_e2 should now be on e4.")


if __name__ == "__main__":
    PickPlaceDemo().run()
