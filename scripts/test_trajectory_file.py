#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from playback.trajectory import Trajectory

traj = Trajectory()

traj.add(0.0, [0]*14)
traj.add(1.0, [0.1]*14)

traj.save("test_trajectory.json")

traj2 = Trajectory.load("test_trajectory.json")

print(len(traj2.waypoints))
