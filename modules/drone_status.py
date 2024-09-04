"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Simple enumeration about the status of the drone.
"""

import enum


class DroneStatus(enum.Enum):
    """
    Status of drone.
    """

    MOVING = 0  # Moving towards destination
    HALTED = 1  # Not moving
    LANDED = 2  # On ground
