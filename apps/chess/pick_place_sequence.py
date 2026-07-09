#!/usr/bin/env python3

from manipulation.planning.task_sequence import (
    EndEffectorOrientation,
    ManipulationTaskSequence,
    ManipulationWaypoint,
)
from apps.chess.board_geometry import Vector3D
from apps.chess.task_builder import PickPlaceTask


def wrist_parallel_to_board_orientation() -> EndEffectorOrientation:
    return EndEffectorOrientation(
        name="wrist_parallel_to_board",
        approach_axis=Vector3D(x=0.0, y=0.0, z=-1.0),
        wrist_parallel_axis=Vector3D(x=1.0, y=0.0, z=0.0),
    )


def chess_pick_place_to_sequence(task: PickPlaceTask) -> ManipulationTaskSequence:
    orientation = wrist_parallel_to_board_orientation()

    return ManipulationTaskSequence(
        waypoints=[
            ManipulationWaypoint(
                name=f"approach_{task.source_square}",
                position=task.source_approach,
                gripper_closed=False,
                orientation=orientation,
            ),
            ManipulationWaypoint(
                name=f"pick_{task.source_square}",
                position=task.source_pick,
                gripper_closed=False,
                orientation=orientation,
            ),
            ManipulationWaypoint(
                name=f"grasp_{task.source_square}",
                position=task.source_pick,
                gripper_closed=True,
                orientation=orientation,
            ),
            ManipulationWaypoint(
                name=f"lift_{task.source_square}",
                position=task.source_approach,
                gripper_closed=True,
                orientation=orientation,
            ),
            ManipulationWaypoint(
                name=f"approach_{task.target_square}",
                position=task.target_approach,
                gripper_closed=True,
                orientation=orientation,
            ),
            ManipulationWaypoint(
                name=f"place_{task.target_square}",
                position=task.target_place,
                gripper_closed=True,
                orientation=orientation,
            ),
            ManipulationWaypoint(
                name=f"release_{task.target_square}",
                position=task.target_place,
                gripper_closed=False,
                orientation=orientation,
            ),
            ManipulationWaypoint(
                name=f"retract_{task.target_square}",
                position=task.target_approach,
                gripper_closed=False,
                orientation=orientation,
            ),
        ]
    )
