#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from planning.tasks.tasks import *

print(PickTask("e2"))
print(PlaceTask("e4"))
print(CupTask("cup"))
