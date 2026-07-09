import time
import mujoco
import mujoco.viewer

path = "simulation/urdf/g1_d_with_dex1_1_fixed.urdf"
model = mujoco.MjModel.from_xml_path(path)
data = mujoco.MjData(model)

print("Loaded:", path)
print("nq:", model.nq, "nv:", model.nv, "nu:", model.nu)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(1 / 60)
