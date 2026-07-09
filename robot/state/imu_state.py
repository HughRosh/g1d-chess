#!/usr/bin/env python3

from dataclasses import dataclass, field
import numpy as np


@dataclass
class IMUState:
    rpy: np.ndarray = field(default_factory=lambda: np.zeros(3))
    omega: np.ndarray = field(default_factory=lambda: np.zeros(3))
