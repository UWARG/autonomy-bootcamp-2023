"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def dist_sq(self, location1: location.Location, location2: location.Location) -> float:
        """
        Calculates the squared Euclidean distance between two locations.
        """
        return (location1.location_x - location2.location_x) ** 2 + (
            location1.location_y - location2.location_y
        ) ** 2

    def clamp(self, val: float, min_val: float, max_val: float) -> float:
        """
        Clamps a value between a lower and upper bound.
        """
        return min(max_val, max(min_val, val))

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        if report.status == drone_status.DroneStatus.HALTED:
            dist_waypoint_sq = self.dist_sq(self.waypoint, report.position)
            if dist_waypoint_sq < self.acceptance_radius**2:
                command = commands.Command.create_land_command()
            else:
                rel_x = self.clamp(self.waypoint.location_x - report.position.location_x, -60, 60)
                rel_y = self.clamp(self.waypoint.location_y - report.position.location_y, -60, 60)
                command = commands.Command.create_set_relative_destination_command(rel_x, rel_y)

        # Do something based on the report and the state of this class...
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
