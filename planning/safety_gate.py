#!/usr/bin/env python3

def require_real_robot_confirmation(backend, allow_real=False):
    if backend == "real" and not allow_real:
        raise RuntimeError(
            "Real robot execution blocked. "
            "Re-run with --allow-real only after the robot area is clear."
        )
