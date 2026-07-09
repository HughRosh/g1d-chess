#!/usr/bin/env python3

import numpy as np
import pinocchio as pin


def se3_from_xyz_quat(position_xyz, orientation_xyzw):
    x, y, z, w = orientation_xyzw
    quat = pin.Quaternion(w, x, y, z)
    quat.normalize()

    return pin.SE3(
        quat.toRotationMatrix(),
        np.asarray(position_xyz, dtype=float),
    )


def pose_error(current, target):
    return pin.log6(current.inverse() * target).vector
