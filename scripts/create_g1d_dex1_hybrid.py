import copy
import xml.etree.ElementTree as ET
from pathlib import Path

G1D_URDF = Path("simulation/urdf/g1_d.urdf")
DEX_URDF = Path("simulation/urdf/g1_d_dex1_1.urdf")
OUT_URDF = Path("simulation/urdf/g1_d_with_dex1_1_hybrid.urdf")

HAND_PREFIXES = (
    "left_hand_",
    "right_hand_",
    "left_dex1_",
    "right_dex1_",
)

HAND_JOINTS = (
    "left_hand_palm_joint",
    "left_hand_thumb_0_joint",
    "left_hand_thumb_1_joint",
    "left_hand_thumb_2_joint",
    "left_hand_middle_0_joint",
    "left_hand_middle_1_joint",
    "left_hand_index_0_joint",
    "left_hand_index_1_joint",
    "right_hand_palm_joint",
    "right_hand_thumb_0_joint",
    "right_hand_thumb_1_joint",
    "right_hand_thumb_2_joint",
    "right_hand_middle_0_joint",
    "right_hand_middle_1_joint",
    "right_hand_index_0_joint",
    "right_hand_index_1_joint",
)

DEX_NAMES = (
    "left_base_joint",
    "left_dex1_base_link",
    "left_dex1_finger_link_1",
    "left_dex1_finger_joint_1",
    "left_dex1_finger_link_2",
    "left_dex1_finger_joint_2",
    "right_base_joint",
    "right_dex1_base_link",
    "right_dex1_finger_link_1",
    "right_dex1_finger_joint_1",
    "right_dex1_finger_link_2",
    "right_dex1_finger_joint_2",
)


def should_remove_from_g1d(elem):
    name = elem.attrib.get("name", "")

    if name in HAND_JOINTS:
        return True

    if any(name.startswith(prefix) for prefix in HAND_PREFIXES):
        return True

    return False


def main():
    g1d_tree = ET.parse(G1D_URDF)
    g1d_root = g1d_tree.getroot()

    dex_tree = ET.parse(DEX_URDF)
    dex_root = dex_tree.getroot()

    for elem in list(g1d_root):
        if elem.tag in ("link", "joint") and should_remove_from_g1d(elem):
            g1d_root.remove(elem)

    dex_elements = []
    for elem in dex_root:
        name = elem.attrib.get("name", "")
        if name in DEX_NAMES:
            dex_elements.append(copy.deepcopy(elem))

    for elem in dex_elements:
        g1d_root.append(elem)

    g1d_root.set("name", "g1_d_with_dual_dex1_1_hybrid")

    ET.indent(g1d_tree, space="  ")
    g1d_tree.write(OUT_URDF, encoding="utf-8", xml_declaration=True)

    print(f"Wrote {OUT_URDF}")
    print("Removed both G1-D dexterous hands and added left/right Dex1_1 grippers.")


if __name__ == "__main__":
    main()
