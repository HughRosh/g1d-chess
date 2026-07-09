from pathlib import Path
import time

import mujoco
import mujoco.viewer
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "simulation" / "urdf" / "g1d_chess_robot_piece_scene.urdf"

PIECE_JOINT = "piece_e2_free"

RIGHT_ARM = {
    "right_shoulder_pitch_joint": 0.0,
    "right_shoulder_roll_joint": -0.3,
    "right_shoulder_yaw_joint": 0.0,
    "right_elbow_joint": 0.8,
    "right_wrist_roll_joint": 0.0,
    "right_wrist_pitch_joint": 0.0,
    "right_wrist_yaw_joint": 0.0,
}

GRIPPER_OPEN = {
    "right_dex1_finger_joint_1": 0.024,
    "right_dex1_finger_joint_2": 0.024,
}

GRIPPER_CLOSED = {
    "right_dex1_finger_joint_1": 0.0,
    "right_dex1_finger_joint_2": 0.0,
}


def joint_addr(model, name):
    jid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name)
    if jid < 0:
        raise KeyError(name)
    return model.jnt_qposadr[jid]


def set_joint(data, model, name, value):
    data.qpos[joint_addr(model, name)] = value


def set_joints(data, model, joints):
    for name, value in joints.items():
        set_joint(data, model, name, value)


def set_piece(data, model, xyz):
    qadr = joint_addr(model, PIECE_JOINT)
    data.qpos[qadr:qadr + 7] = [xyz[0], xyz[1], xyz[2], 1, 0, 0, 0]


def lerp(a, b, t):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return a + (b - a) * t


model = mujoco.MjModel.from_xml_path(str(MODEL))
data = mujoco.MjData(model)

set_joints(data, model, RIGHT_ARM)
set_joints(data, model, GRIPPER_OPEN)

e2 = np.array([0.625, -0.125, 0.7895])
e4 = np.array([0.625, -0.025, 0.7895])

above_e2 = e2 + np.array([0.0, 0.0, 0.18])
above_e4 = e4 + np.array([0.0, 0.0, 0.18])

piece_pos = e2.copy()
carrying = False

print("Launching kinematic robot pick/place demo.")
print("Robot stays upright using mj_forward; piece motion is deterministic e2 -> e4.")

with mujoco.viewer.launch_passive(model, data) as viewer:
    frame = 0
    while viewer.is_running() and frame < 1100:
        frame += 1

        if frame < 180:
            t = frame / 180
            fake_gripper = lerp(above_e2, e2 + [0, 0, 0.055], t)
        elif frame < 240:
            fake_gripper = e2 + [0, 0, 0.055]
            set_joints(data, model, GRIPPER_CLOSED)
            carrying = True
        elif frame < 500:
            t = (frame - 240) / 260
            fake_gripper = lerp(e2 + [0, 0, 0.055], above_e2, t)
        elif frame < 760:
            t = (frame - 500) / 260
            fake_gripper = lerp(above_e2, above_e4, t)
        elif frame < 940:
            t = (frame - 760) / 180
            fake_gripper = lerp(above_e4, e4 + [0, 0, 0.055], t)
        elif frame < 1000:
            fake_gripper = e4 + [0, 0, 0.055]
            carrying = False
            set_joints(data, model, GRIPPER_OPEN)
            piece_pos = e4.copy()
        else:
            fake_gripper = above_e4

        # simple visible arm motion while the deterministic gripper path runs
        set_joint(data, model, "right_shoulder_roll_joint", -0.3 + 0.15 * np.sin(frame / 160))
        set_joint(data, model, "right_elbow_joint", 0.8 + 0.25 * np.sin(frame / 220))

        if carrying:
            piece_pos = fake_gripper - np.array([0.0, 0.0, 0.055])

        set_piece(data, model, piece_pos)

        mujoco.mj_forward(model, data)
        viewer.sync()
        time.sleep(0.002)

print("Done. piece_e2 should finish on e4.")
