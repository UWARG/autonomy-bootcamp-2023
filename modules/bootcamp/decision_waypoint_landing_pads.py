"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.

        Args:
            waypoint (location.Location): The waypoint location to travel to.
            acceptance_radius (float): The radius within which the waypoint is considered reached.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        print(str(waypoint.location_x) + str(waypoint.location_y))

        self.has_sent_landing_command = False
        self.find_nearest_landing_pad = False
        self.reached_waypoint = False
        self.moving_to_landing_pad = False
        self.counter = 0

    def at_point(self, current_x: float, current_y: float) -> bool:
        """
        Check if the current position is within the acceptance radius of the waypoint.

        Args:
            current_x (float): The current x-coordinate of the drone.
            current_y (float): The current y-coordinate of the drone.

        Returns:
            bool: True if the drone is within the acceptance radius, False otherwise.
        """
        distance_squared = (self.waypoint.location_x - current_x) ** 2 + (
            self.waypoint.location_y - current_y
        ) ** 2
        return distance_squared <= self.acceptance_radius**2

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        Args:
            report (drone_report.DroneReport): Current status report of the drone.
            landing_pad_locations (list[location.Location]): List of available landing pad locations.

        Returns:
            commands.Command: The command for the drone to execute.
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
