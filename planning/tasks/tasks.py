#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class PickTask:
    square: str


@dataclass
class PlaceTask:
    square: str


@dataclass
class MoveTask:
    pose: object


@dataclass
class CupTask:
    object_name: str
