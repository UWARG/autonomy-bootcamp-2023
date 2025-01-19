"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from math import sqrt
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

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # a boolean to see if the drone has reached the waypoint
        self.reached = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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

        status = report.status
        position = report.position

        distance_from_waypoint = sqrt((self.waypoint.location_x - position.location_x) ** 2 + (self.waypoint.location_y - position.location_y) ** 2)

        # if the drone is in the acceptance radius, we have reached
        if distance_from_waypoint < self.acceptance_radius:
            self.reached = True

        if self.reached:
            if status == drone_status.DroneStatus.HALTED:
                return commands.Command.create_land_command()
            return commands.Command.create_halt_command()
        # otherwise, the drone has not reached in the acceptance radius
        # If the drone is not at the waypoint yet
        if status == drone_status.DroneStatus.HALTED:
            relative_destination = location.Location(self.waypoint.location_x - position.location_x, self.waypoint.location_y - position.location_y)
            return commands.Command.create_set_relative_destination_command(relative_destination.location_x, relative_destination.location_y)

        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
