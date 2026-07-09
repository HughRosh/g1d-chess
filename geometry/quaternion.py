#!/usr/bin/env python3

import numpy as np
import math


def normalize(q):
    q = np.asarray(q, dtype=float)
    return q / np.linalg.norm(q)


def multiply(q1, q2):
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2

    return np.array([
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
    ])


def from_yaw(yaw):

    h = yaw * 0.5

    return np.array([
        0.0,
        0.0,
        math.sin(h),
        math.cos(h),
    ])


def identity():
    return np.array([0.,0.,0.,1.])
