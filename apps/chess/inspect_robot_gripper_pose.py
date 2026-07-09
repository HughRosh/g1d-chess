from pathlib import Path
import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "simulation" / "urdf" / "g1d_chess_robot_piece_scene.urdf"

model = mujoco.MjModel.from_xml_path(str(MODEL))
data = mujoco.MjData(model)

def body_xyz(name):
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
    if bid < 0:
        raise KeyError(name)
    return data.xpos[bid].copy()

mujoco.mj_forward(model, data)

a = body_xyz("right_dex1_finger_link_1")
b = body_xyz("right_dex1_finger_link_2")
mid = (a + b) / 2

print("finger 1:", a)
print("finger 2:", b)
print("midpoint:", mid)
print("target e2:", np.array([0.625, -0.125, 0.845]))
print("delta midpoint -> e2:", np.array([0.625, -0.125, 0.845]) - mid)
