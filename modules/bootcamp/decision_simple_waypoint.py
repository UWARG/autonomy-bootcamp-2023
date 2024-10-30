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
        self.position_x = 0
        self.position_y = 0
        self.reached_waypoint = False

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

        def within_acceptance_radius() -> bool:
            return (
                abs(self.waypoint.location_x - self.position_x) <= self.acceptance_radius
                and abs(self.waypoint.location_y - self.position_y) <= self.acceptance_radius
            )

        self.position_x = report.position.location_x
        self.position_y = report.position.location_y
        self.reached_waypoint = within_acceptance_radius()

        if report.status == drone_status.DroneStatus.HALTED and not self.reached_waypoint:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x,
                self.waypoint.location_y,
            )

        elif report.status == drone_status.DroneStatus.HALTED and self.reached_waypoint:
            command = commands.Command.create_land_command()

        elif report.status == drone_status.DroneStatus.MOVING and self.reached_waypoint:
            command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
