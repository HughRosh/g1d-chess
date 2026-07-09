#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Box:
    size: tuple


@dataclass
class Cylinder:
    radius: float
    height: float
