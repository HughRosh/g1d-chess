#!/usr/bin/env python3

from pathlib import Path
import numpy as np
import pinocchio as pin

from robot.kinematics.ik import se3_from_xyz_quat, pose_error


class G1DKinematics:
    def __init__(self, end_effector_frame="right_dex1_base_link"):
        urdf = Path("simulation/urdf/g1_d_with_dex1_1_hybrid.urdf")

        self.model = pin.buildModelFromUrdf(str(urdf))
        self.data = self.model.createData()

        self.ee_frame_name = end_effector_frame
        self.ee_frame_id = self.model.getFrameId(self.ee_frame_name)

    def neutral_q(self):
        return pin.neutral(self.model)

    def frame_placement(self, q=None):
        if q is None:
            q = self.neutral_q()

        pin.forwardKinematics(self.model, self.data, q)
        pin.updateFramePlacements(self.model, self.data)

        return self.data.oMf[self.ee_frame_id]

    def forward_kinematics(self, q=None):
        placement = self.frame_placement(q)

        return {
            "position_xyz": placement.translation.tolist(),
            "rotation_matrix": placement.rotation.tolist(),
        }

    def solve_pose_ik(self, target_pose, q0=None, max_iters=300, tol=1e-3):
        q = self.neutral_q() if q0 is None else q0.copy()

        target = se3_from_xyz_quat(
            target_pose.position_xyz,
            target_pose.orientation_xyzw,
        )

        damping = 1e-4
        step_scale = 0.35

        for i in range(max_iters):
            current = self.frame_placement(q)
            err = pose_error(current, target)

            if np.linalg.norm(err) < tol:
                return q, True, i, float(np.linalg.norm(err))

            J = pin.computeFrameJacobian(
                self.model,
                self.data,
                q,
                self.ee_frame_id,
                pin.ReferenceFrame.LOCAL,
            )

            dq = J.T @ np.linalg.solve(
                J @ J.T + damping * np.eye(6),
                err,
            )

            q = pin.integrate(self.model, q, step_scale * dq)

        return q, False, max_iters, float(np.linalg.norm(err))

    def solve_position_ik(self, target_xyz, q0=None, max_iters=200, tol=1e-3):
        q = self.neutral_q() if q0 is None else q0.copy()
        target = np.asarray(target_xyz, dtype=float)

        damping = 1e-4
        step_scale = 0.5

        for i in range(max_iters):
            current = self.frame_placement(q).translation
            error = target - current

            if np.linalg.norm(error) < tol:
                return q, True, i, float(np.linalg.norm(error))

            J6 = pin.computeFrameJacobian(
                self.model,
                self.data,
                q,
                self.ee_frame_id,
                pin.ReferenceFrame.LOCAL_WORLD_ALIGNED,
            )

            J = J6[:3, :]

            dq = J.T @ np.linalg.solve(
                J @ J.T + damping * np.eye(3),
                error,
            )

            q = pin.integrate(self.model, q, step_scale * dq)

        return q, False, max_iters, float(np.linalg.norm(error))
