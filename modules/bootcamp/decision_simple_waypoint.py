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

        self.command = commands.Command.create_set_relative_destination_command(
            waypoint.location_x, waypoint.location_y
        )

        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
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

        # Do something based on the report and the state of this class...

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(
            self.commands
        ):
            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and (
            (report.position.location_x - self.waypoint.location_x) > self.acceptance_radius
            or (report.position.location_y - self.waypoint.location_y) > self.acceptance_radius
        ):
            self.counter += 1
        else:
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
