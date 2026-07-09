import os


class G1DBackend:
    """
    Real Unitree G1D backend.

    This file is intentionally safety-gated.
    It will not move hardware unless:

        export G1D_ENABLE_MOTION=1

    Fill the TODO sections with the working robot code you already used.
    """

    def __init__(self):
        self.motion_enabled = os.environ.get("G1D_ENABLE_MOTION") == "1"

    def connect(self):
        print("[G1D] connect")
        print("[G1D] motion enabled:", self.motion_enabled)

        # TODO: paste your known-working Unitree init code here.
        # Example:
        # self.robot = ...
        # self.gripper = ...

    def move_joints(self, joint_positions, duration=2.0):
        print("[G1D] requested move_joints")
        print("duration:", duration)
        print(joint_positions)

        if not self.motion_enabled:
            print("[G1D SAFETY] Motion disabled. Set G1D_ENABLE_MOTION=1 on robot to move.")
            return

        # TODO: paste your known-working joint command code here.
        # Send only validated joint names/positions.

    def open_gripper(self):
        print("[G1D] requested open_gripper")

        if not self.motion_enabled:
            print("[G1D SAFETY] Motion disabled. Not opening gripper.")
            return

        # TODO: paste your known-working gripper open code here.

    def close_gripper(self):
        print("[G1D] requested close_gripper")

        if not self.motion_enabled:
            print("[G1D SAFETY] Motion disabled. Not closing gripper.")
            return

        # TODO: paste your known-working gripper close code here.

    def stop(self):
        print("[G1D] stop requested")

        # TODO: paste damping/emergency stop code here if you have it.
