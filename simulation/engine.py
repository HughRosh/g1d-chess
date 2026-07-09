from __future__ import annotations

from pathlib import Path
import time

import mujoco
import mujoco.viewer
import numpy as np


class MujocoEngine:
    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self.model = mujoco.MjModel.from_xml_path(str(self.model_path))
        self.data = mujoco.MjData(self.model)
        mujoco.mj_forward(self.model, self.data)

    def joint_qpos_addr(self, joint_name: str) -> int:
        jid = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)
        if jid < 0:
            raise KeyError(f"Joint not found: {joint_name}")
        return int(self.model.jnt_qposadr[jid])

    def set_free_joint_pose(
        self,
        joint_name: str,
        xyz: tuple[float, float, float],
        quat_wxyz: tuple[float, float, float, float] = (1.0, 0.0, 0.0, 0.0),
    ) -> None:
        qadr = self.joint_qpos_addr(joint_name)
        self.data.qpos[qadr : qadr + 3] = xyz
        self.data.qpos[qadr + 3 : qadr + 7] = quat_wxyz
        mujoco.mj_forward(self.model, self.data)

    def get_free_joint_xyz(self, joint_name: str) -> np.ndarray:
        qadr = self.joint_qpos_addr(joint_name)
        return self.data.qpos[qadr : qadr + 3].copy()


    def body_id(self, body_name: str) -> int:
        bid = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, body_name)
        if bid < 0:
            raise KeyError(f"Body not found: {body_name}")
        return int(bid)

    def get_body_xyz(self, body_name: str) -> np.ndarray:
        bid = self.body_id(body_name)
        return self.data.xpos[bid].copy()

    def step(self, n: int = 1) -> None:
        for _ in range(n):
            mujoco.mj_step(self.model, self.data)

    def launch(self, callback) -> None:
        with mujoco.viewer.launch_passive(self.model, self.data) as viewer:
            while viewer.is_running():
                done = callback()
                mujoco.mj_step(self.model, self.data)
                viewer.sync()
                time.sleep(0.002)
                if done:
                    time.sleep(2.0)
                    break
