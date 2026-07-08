import time
from pathlib import Path
import math

import mujoco
import mujoco.viewer

MODEL_PATH = Path("simulation/urdf/g1d_chess_static_scene.urdf")

RIGHT_ARM_JOINTS = {
    "right_shoulder_pitch_joint": (-0.2, -0.9),
    "right_shoulder_roll_joint": (-0.2, -0.45),
    "right_shoulder_yaw_joint": (0.0, 0.25),
    "right_elbow_joint": (0.6, 1.25),
    "right_wrist_roll_joint": (0.0, 0.0),
    "right_wrist_pitch_joint": (0.0, -0.45),
    "right_wrist_yaw_joint": (0.0, 0.0),
}

GRIPPER_JOINTS = {
    "right_dex1_finger_joint_1": (0.0245, -0.005),
    "right_dex1_finger_joint_2": (0.0245, -0.005),
}


def set_joint(model, data, joint_name, value):
    joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)
    if joint_id < 0:
        print(f"Missing joint: {joint_name}")
        return

    qpos_addr = model.jnt_qposadr[joint_id]
    data.qpos[qpos_addr] = value


def geom_name(model, geom_id):
    if geom_id < 0:
        return "unknown"
    return mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, geom_id)


def print_contacts(model, data):
    if data.ncon == 0:
        return

    print(f"\nCONTACTS: {data.ncon}")
    for i in range(data.ncon):
        c = data.contact[i]
        g1 = geom_name(model, c.geom1)
        g2 = geom_name(model, c.geom2)
        print(f"  {g1} <-> {g2}, dist={c.dist:.4f}")


def main():
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)

    print(f"Loaded scene: {MODEL_PATH}")
    print("Animating right arm + Dex1_1 gripper.")
    print("This is kinematic preview; collisions are reported, not prevented.")

    last_contact_print = 0.0

    with mujoco.viewer.launch_passive(model, data) as viewer:
        start = time.time()

        while viewer.is_running():
            t = time.time() - start
            alpha = 0.5 * (1.0 - math.cos(t * 0.8))

            for joint, (home, reach) in RIGHT_ARM_JOINTS.items():
                value = home + alpha * (reach - home)
                set_joint(model, data, joint, value)

            grip_alpha = 0.5 * (1.0 - math.cos(t * 1.4))
            for joint, (open_pos, closed_pos) in GRIPPER_JOINTS.items():
                value = open_pos + grip_alpha * (closed_pos - open_pos)
                set_joint(model, data, joint, value)

            mujoco.mj_forward(model, data)

            if data.ncon > 0 and t - last_contact_print > 1.0:
                print_contacts(model, data)
                last_contact_print = t

            viewer.sync()
            time.sleep(0.01)


if __name__ == "__main__":
    main()
