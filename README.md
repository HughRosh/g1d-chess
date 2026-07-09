# G1-D Chess

A robotics framework for autonomous chess using the Unitree G1-D humanoid robot equipped with Dex1.1 grippers.

The goal of this project is to build a complete perception, planning, and manipulation stack capable of playing chess autonomously while maintaining a hardware-independent software architecture.

The exact same chess planner should execute on:

- Mock Controller
- MuJoCo Simulation
- Physical Unitree G1-D

by changing only the controller backend.

---

# Features

## Simulation

- Hybrid G1-D robot model
- Configurable table
- Configurable chessboard
- Configurable cup
- Top-down manipulation constraints
- MuJoCo visualization
- Mock hardware backend

## Hardware

Verified on a physical Unitree G1-D

- DDS communication
- ROS2 Foxy integration
- Internal G1-D controller wrapper
- Real arm control
- Real Dex1.1 gripper control
- Joint state feedback
- Backend abstraction layer

---

# Repository Layout

```
configs/

hardware/
    g1d/
        controller.py
        mock_controller.py
        factory.py
        test_controller.py
        test_mock_controller.py

planning/

robot/

scripts/

simulation/
    mujoco/
    urdf/

vision/

README.md
```

---

# Architecture

```
                 Chess Engine
                      │
                      ▼
              Motion Planner
                      │
                      ▼
             Controller Interface
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
 Mock Controller            Real G1-D Controller
        │                           │
        ▼                           ▼
 MuJoCo Simulation         Unitree Internal SDK
```

The chess engine never communicates directly with the Unitree SDK.

Only the controller backend changes.

---

# Controller Backends

Mock

```python
from hardware.g1d.factory import make_g1d_controller

robot = make_g1d_controller("mock")
```

Real Robot

```python
from hardware.g1d.factory import make_g1d_controller

robot = make_g1d_controller(
    backend="real",
    interface="eth0"
)
```

---

# Current Controller API

```python
robot.current_arm()

robot.move_joint(...)

robot.move_arm(...)

robot.open_gripper()

robot.close_gripper()

robot.home()
```

Future API

```python
robot.move_pose(...)

robot.pick(...)

robot.place(...)

robot.execute_move(...)
```

The long-term goal is for the chess planner to never manipulate joints directly.

Instead it will simply request Cartesian motions.

---

# Current Progress

## Completed

- Hybrid G1-D URDF
- Dual Dex1.1 integration
- Configurable simulation scene
- Top-down manipulation constraints
- MuJoCo visualization
- Physical arm control
- Physical gripper control
- Mock controller
- Hardware controller wrapper
- Backend selector

## In Progress

- Cartesian pose controller
- Workspace calibration
- Inverse kinematics

## Planned

- Chessboard calibration
- Camera integration
- Chess piece detection
- Motion planning
- Pick and place
- Complete autonomous chess gameplay

---

# Hardware

Verified Hardware

- Unitree G1-D
- Dex1.1 Grippers
- ROS2 Foxy
- Unitree SDK2
- DDS
- Ethernet (eth0)

---

# Design Philosophy

Every feature should be developed in simulation first.

When validated, the exact same planner should execute on the real robot without modification.

```
Simulation

↓

Hardware Wrapper

↓

Real Robot
```

The controller layer is the only component that knows whether the robot is simulated or physical.

---

# Long-Term Vision

Although this project currently focuses on autonomous chess, the architecture is designed to support any tabletop manipulation task.

Future capabilities include:

- Cup manipulation
- Object sorting
- Warehouse picking
- Tool use
- Household manipulation
- Human-robot collaboration

The long-term objective is to create a reusable manipulation framework for the Unitree G1-D.

---

# Acknowledgements

This project builds upon:

- Unitree SDK2
- ROS2 Foxy
- MuJoCo
- Python
- Custom G1-D hardware controller abstraction

---

# Status

Current repository maturity:

Simulation:
- Working

Hardware:
- Working

Mock backend:
- Working

Real arm control:
- Verified

Real Dex1.1 gripper control:
- Verified

Current focus:

Building a complete hardware-independent manipulation framework capable of autonomous chess.
