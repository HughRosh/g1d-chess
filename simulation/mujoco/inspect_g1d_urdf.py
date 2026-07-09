import mujoco

path = "simulation/urdf/g1_d_with_dex1_1_fixed.urdf"
model = mujoco.MjModel.from_xml_path(path)

print("Loaded:", path)
print("nq:", model.nq, "nv:", model.nv, "nu:", model.nu)
print("\nJoints:")
for i in range(model.njnt):
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
    lo, hi = model.jnt_range[i]
    print(i, name, "range:", float(lo), float(hi))
