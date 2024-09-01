"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

The current state of the drone.
"""

from . import drone_status
from . import location


class DroneReport:
    """
    Information about current state.
    """

    def __init__(
        self,
        status: drone_status.DroneStatus,
        destination: location.Location,
        position: location.Location,
    ) -> None:
        """
        Construct report on the state of the drone.
        """
        self.status = status
        self.destination = destination
        self.position = position

    def __eq__(self, other: "DroneReport") -> bool:
        """
        Required for comparison.
        """
        if not isinstance(other, DroneReport):
            return False

        if not self.status == other.status:
            return False

        if not self.destination == other.destination:
            return False

        if not self.position == other.position:
            return False

        return True

    def __hash__(self) -> int:
        """
        Required for dictionaries and sets.
        """
        return hash((self.status, self.destination, self.position))

    def __repr__(self) -> str:
        """
        To string.
        """
        representation = (
            f"DRONE REPORT:\n"
            f"Status: {self.status}\n"
            f"Position: {self.position}\n"
            f"Destination: {self.destination}\n"
        )

        return representation
