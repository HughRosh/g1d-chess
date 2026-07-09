#!/usr/bin/env python3

import sys
import time
from multiprocessing import Value

import numpy as np

sys.path.append("/home/unitree")

from test_g1_dex1_internal import G1_29_Arm_Internal_Dex1_Controller
from unitree_sdk2py.core.channel import ChannelFactoryInitialize


class G1DController:
    def __init__(self, interface="eth0"):
        ChannelFactoryInitialize(0, interface)

        self.left_gripper = Value("d", 7.0, lock=True)
        self.right_gripper = Value("d", 7.0, lock=True)

        self.ctrl = G1_29_Arm_Internal_Dex1_Controller(
            self.left_gripper,
            self.right_gripper,
        )

    def current_arm(self):
        return self.ctrl.get_current_dual_arm_q().copy()

    def move_arm(self, q, seconds=3.0):
        q = np.array(q, dtype=float)

        for _ in range(int(seconds * 100)):
            self.ctrl.ctrl_dual_arm(q, np.zeros(14))
            time.sleep(0.01)

    def move_joint(self, joint_index, delta, seconds=3.0):
        q = self.current_arm()
        q[joint_index] += delta
        self.move_arm(q, seconds=seconds)

    def open_gripper(self):
        self.left_gripper.value = 7.0
        self.right_gripper.value = 7.0

    def close_gripper(self):
        self.left_gripper.value = 5.37
        self.right_gripper.value = 5.37

    def home(self):
        q = self.current_arm()
        q[:] = 0.0
        self.move_arm(q, seconds=3.0)
