from pathlib import Path
import time

import mujoco
import mujoco.viewer

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "simulation" / "urdf" / "g1_d_with_dex1_1_hybrid.urdf"

model = mujoco.MjModel.from_xml_path(str(MODEL))
data = mujoco.MjData(model)

print("Loaded robot-only scene")
print("nq:", model.nq, "nv:", model.nv, "nbody:", model.nbody)

with mujoco.viewer.launch_passive(model, data) as viewer:
    start = time.time()
    while viewer.is_running() and time.time() - start < 8:
        mujoco.mj_forward(model, data)
        viewer.sync()
        time.sleep(0.002)
