# G1-D Low-Level Control Background

DDS topics:

- Command: `rt/lowcmd`
- State: `rt/lowstate`
- Torso IMU: `rt/secondary_imu`

The G1-D low-level command array has 29 motor slots.

Valid upper-body motors:

- Waist yaw: 12
- Waist pitch: 14
- Left arm: 15–21
- Right arm: 22–28

Invalid leg indices remain present in the array but are not used for G1-D.

The C++ Unitree example initializes DDS, subscribes to low state and IMU, waits for controller button A, then writes `LowCmd_` messages with position targets, kp, kd, and CRC.
