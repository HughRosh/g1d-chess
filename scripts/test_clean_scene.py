from pathlib import Path
import mujoco

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "simulation" / "mujoco" / "g1d_chess_scene.xml"

model = mujoco.MjModel.from_xml_path(str(MODEL))
print("Loaded:", MODEL)
print("nbody:", model.nbody)
print("njnt:", model.njnt)
