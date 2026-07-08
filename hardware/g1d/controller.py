#!/usr/bin/env python3

"""
G1-D Hardware Controller

Thin wrapper around the Unitree internal Dex1.1 controller.

This file intentionally hides all Unitree SDK details from the
rest of the project.

Future project code should ONLY call methods on G1DController.
"""

import sys
import time
from multiprocessing import Value
import numpy as np

# Path on the robot
sys.path.append("/home/unitree")

from test_g1_dex1_internal import (
    G1_29_Arm_Internal_Dex1_Controller,
)

from unitree_sdk2py.core.channel import ChannelFactoryInitialize


class G1DController:

    def __init__(self, interface="eth0"):

        ChannelFactoryInitialize(0, interface)

        self.left_gripper = Value("d", 7.0, lock=True)
        self.right_gripper = Value("d", 7.0, lock=True)

        self.ctrl = G1_29_Arm_Internal_Dex1_Controller(
            self.left_gripper,
            self.right_gripper
        )

    ####################################################
    # ARM
    ####################################################

    def current_arm(self):
        return self.ctrl.get_current_dual_arm_q().copy()

    def move_arm(self, q, seconds=3.0):

        q = np.array(q, dtype=float)

        for _ in range(int(seconds * 100)):
            self.ctrl.ctrl_dual_arm(q, np.zeros(14))
            time.sleep(0.01)

    def move_joint(self, joint, delta):

        q = self.current_arm()
        q[joint] += delta
        self.move_arm(q)

    ####################################################
    # GRIPPER
    ####################################################

    def open_gripper(self):

        self.left_gripper.value = 7.0
        self.right_gripper.value = 7.0

    def close_gripper(self):

        self.left_gripper.value = 5.37
        self.right_gripper.value = 5.37

    ####################################################
    # HOME
    ####################################################

    def home(self):

        q = self.current_arm()

        for i in range(len(q)):
            q[i] = 0.0

        self.move_arm(q)

