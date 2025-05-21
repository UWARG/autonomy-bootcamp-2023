"""
BOOTCAMPERS TO COMPLETE.

Test decision example.

You can change the timestep, display scale, and seed, if you wish.
Do not modify anything else.
"""

import time

from modules.bootcamp.tests.private import decision_factory
from modules.bootcamp.tests.private import runner


# ============
# ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# ============

# Ideally, it takes 12.5 seconds of wall clock time
# to reach the 1st command
# Increase the step size if your computer is lagging
# Larger step size is smaller FPS
TIME_STEP_SIZE = 0.2  # seconds

# OpenCV ignores your display settings,
# so if the window is too small or too large,
# change this value (between 0.0 and 1.0)
DISPLAY_SCALE = 0.8

# Seed for randomly generating the waypoint and landing pad
# Change to a constant for reproducibility (e.g. debugging)
# Change back to = time.time_ns() to test robustness
SEED = time.time_ns()

# ============
# ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# ============


def main() -> int:
    """
    main.
    """
    # Run
    return runner.runner(decision_factory.DecisionEnum.EXAMPLE, TIME_STEP_SIZE, DISPLAY_SCALE, SEED)


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
