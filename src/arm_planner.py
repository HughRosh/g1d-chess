def make_pick_place_motion(plan, config):
    safe_z = config["motion"]["safe_z_m"]
    pick_z = config["motion"]["pick_z_m"]

    px, py = plan["pick_xy"]
    qx, qy = plan["place_xy"]

    return [
        {"action": "move", "target": [px, py, safe_z]},
        {"action": "move", "target": [px, py, pick_z]},
        {"action": "gripper", "state": "close"},
        {"action": "move", "target": [px, py, safe_z]},
        {"action": "move", "target": [qx, qy, safe_z]},
        {"action": "move", "target": [qx, qy, pick_z]},
        {"action": "gripper", "state": "open"},
        {"action": "move", "target": [qx, qy, safe_z]},
    ]
