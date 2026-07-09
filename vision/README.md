# Vision Pipeline

The vision system is responsible only for perception.

It does **NOT** decide what to do.

Pipeline:

Camera
    ↓
Calibration
    ↓
Board Localization
    ↓
Piece Detection
    ↓
Object Localization
    ↓
World Model

Outputs:

- Board pose (SE3)
- Piece poses (SE3)
- Confidence
- Camera pose

Consumers:

- Decision
- Manipulation
- Simulator
