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

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own
        self.acceptance_radius = acceptance_radius
        self.distance_y = 0
        self.distance_x = 0
        self.distance = 0
        self.reached_destination = False

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

        self.distance_x = report.position.location_x - self.waypoint.location_x
        self.distance_y = report.position.location_y - self.waypoint.location_y
        self.distance = ((self.distance_x) ** 2 + (self.distance_y) ** 2) ** 0.5
        # self.reached_destination = False

        # halt the drone when the destination is reached
        if self.distance < self.acceptance_radius:
            if drone_status.DroneStatus.HALTED:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_halt_command()
                self.reached_destination = True

        # land the drone and sit there
        elif self.reached_destination and drone_status == drone_status.DroneStatus.LANDED:
            command = commands.Command.create_null_command()

        # check if drone is at origin and move to waypoint
        elif not self.reached_destination and (
            report.position.location_x == 0 and report.position.location_y == 0
        ):
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
