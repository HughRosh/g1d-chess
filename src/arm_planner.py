SAFE_Z = 0.20
PICK_Z = 0.03

def make_pick_place_motion(plan):
    px, py = plan["pick_xy"]
    qx, qy = plan["place_xy"]

    return [
        {"action": "move", "target": [px, py, SAFE_Z]},
        {"action": "move", "target": [px, py, PICK_Z]},
        {"action": "gripper", "state": "close"},
        {"action": "move", "target": [px, py, SAFE_Z]},
        {"action": "move", "target": [qx, qy, SAFE_Z]},
        {"action": "move", "target": [qx, qy, PICK_Z]},
        {"action": "gripper", "state": "open"},
        {"action": "move", "target": [qx, qy, SAFE_Z]},
    ]
