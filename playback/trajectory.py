#!/usr/bin/env python3

from dataclasses import dataclass, field
import json


@dataclass
class Waypoint:
    time_s: float
    joint_positions: list


@dataclass
class Trajectory:
    waypoints: list = field(default_factory=list)

    def add(self, t, q):
        self.waypoints.append(
            Waypoint(
                float(t),
                list(q),
            )
        )

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(
                [
                    {
                        "time": w.time_s,
                        "joint_positions": w.joint_positions,
                    }
                    for w in self.waypoints
                ],
                f,
                indent=2,
            )

    @staticmethod
    def load(filename):

        with open(filename) as f:
            data = json.load(f)

        traj = Trajectory()

        for w in data:
            traj.add(
                w["time"],
                w["joint_positions"],
            )

        return traj
