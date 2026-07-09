from pathlib import Path
import mujoco

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "simulation" / "urdf" / "g1d_chess_robot_piece_scene.urdf"

model = mujoco.MjModel.from_xml_path(str(MODEL))

print("Bodies containing right/dex/wrist/finger:")
for i in range(model.nbody):
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i)
    if name and any(s in name.lower() for s in ["right", "dex", "wrist", "finger"]):
        print(i, name)

print("\nJoints containing right/dex/wrist/finger:")
for i in range(model.njnt):
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
    if name and any(s in name.lower() for s in ["right", "dex", "wrist", "finger"]):
        print(i, name, "qposadr=", model.jnt_qposadr[i])
