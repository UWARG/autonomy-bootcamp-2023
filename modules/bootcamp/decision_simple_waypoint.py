"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from .. import commands
from .. import drone_report
import math
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
        print(self.acceptance_radius)
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y),
     
        ]

        self.has_sent_landing_command = False

        self.counter = 0

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

        

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(
            self.commands
        ):
            # Print some information for debugging
            print(self.counter)
            print(self.command_index)
            print(f"Halted at: {report.position}")

            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command and check_radius(report.position.location_x, report.position.location_y, self.waypoint.location_x, self.waypoint.location_y) :
            command = commands.Command.create_land_command()

            self.has_sent_landing_command = True

        self.counter += 1

        def check_radius(current_x, current_y, waypoint_x, waypoint_y):
            radius = math.sqrt((waypoint_x - current_x) ** 2 + (waypoint_y - current_y) ** 2)

            return radius < self.acceptance_radius

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
