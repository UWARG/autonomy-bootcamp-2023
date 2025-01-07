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

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def get_x_difference(self, initial: location.Location, final: location.Location) -> float:
        """
        Get the difference in x values from initial and final locations.
        """
        return final.location_x - initial.location_x

    def get_y_difference(self, initial: location.Location, final: location.Location) -> float:
        """
        Get the difference in y values from initial and final locations.
        """
        return final.location_y - initial.location_y

    def get_distance_squared(self, diff_x: float, diff_y: float) -> float:
        """
        Return the distance squared of two locations based on their difference in x and y values.
        """
        return diff_x**2 + diff_y**2

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

        x_difference = self.get_x_difference(report.position, self.waypoint)
        y_difference = self.get_y_difference(report.position, self.waypoint)

        if report.status == drone_status.DroneStatus.MOVING:
            command = commands.Command.create_null_command()
        elif self.get_distance_squared(x_difference, y_difference) >= (
            self.acceptance_radius * self.acceptance_radius
        ):
            command = commands.Command.create_set_relative_destination_command(
                x_difference, y_difference
            )
        else:
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
