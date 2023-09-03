"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

The current state of the drone.
"""

from . import drone_status
from . import location


# Basically a struct
# pylint: disable-next=too-few-public-methods
class DroneReport:
    """
    Information about current state.
    """
    def __init__(self,
                 status: drone_status.DroneStatus,
                 destination: location.Location,
                 position: location.Location):
        """
        Construct report on the state of the drone.
        """
        self.status = status
        self.destination = destination
        self.position = position
