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
        self.acceptance_radius_squared = self.acceptance_radius**2  # used for distance calculation

        self.goals = [
            commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
        ]
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def calculate_distance_squared(
        location_1: location.Location, location_2: location.Location
    ) -> float:
        """
        Calculate the non-square rooted distance between two locations
        """
        return (location_2.location_x - location_1.location_x) ** 2 + (
            location_2.location_y - location_1.location_y
        ) ** 2

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

        # Do something based on the report and the state of this class...

        if report.status == drone_status.DroneStatus.HALTED:
            if self.goals:
                command = self.goals.pop(0)
            elif (
                DecisionSimpleWaypoint.calculate_distance_squared(
                    report.position, report.destination
                )
                <= self.acceptance_radius_squared
            ):
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
