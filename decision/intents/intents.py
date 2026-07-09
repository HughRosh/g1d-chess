#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class MovePieceIntent:
    from_square: str
    to_square: str
    capture: bool = False


@dataclass
class PickObjectIntent:
    object_id: str
