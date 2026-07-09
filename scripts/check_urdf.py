#!/usr/bin/env python3

from pathlib import Path
import xml.etree.ElementTree as ET

p = Path("robot/urdf/g1_d.urdf")

if not p.exists():
    raise FileNotFoundError("Missing robot/urdf/g1_d.urdf")

root = ET.parse(p).getroot()

links = root.findall("link")
joints = root.findall("joint")

print("URDF:", p)
print("Robot name:", root.attrib.get("name"))
print("Links:", len(links))
print("Joints:", len(joints))
