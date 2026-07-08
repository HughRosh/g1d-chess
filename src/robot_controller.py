def execute_motion(motion_steps, dry_run=True):
    """
    Placeholder robot controller.

    dry_run=True means print actions only.
    Later this will send commands to the G1-D.
    """
    for i, step in enumerate(motion_steps, start=1):
        print(f"[Robot Step {i}] {step}")

    if dry_run:
        print("Dry run complete. No robot commands were sent.")
