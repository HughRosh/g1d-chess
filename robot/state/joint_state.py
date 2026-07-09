#!/usr/bin/env python3

from dataclasses import dataclass, field
import numpy as np


@dataclass
class JointState:
    q: np.ndarray = field(default_factory=lambda: np.zeros(29))
    dq: np.ndarray = field(default_factory=lambda: np.zeros(29))
