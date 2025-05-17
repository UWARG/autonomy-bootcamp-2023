"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from numpy import sqrt
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

        self.settling_threshold = 10
        self.cycles_at_target = 0  # counts loops passed when drone is within accepted radius

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

        if report.status == drone_status.DroneStatus.HALTED:
            if not self.is_settled(report.position, report.destination):
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x, self.waypoint.location_y
                )
            else:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def is_settled(self, position: location.Location, target: location.Location) -> bool:
        """
        returns if position has been within target for certain amount of loops
        """
        distance = sqrt(
            (target.location_x - position.location_x) ** 2
            + (target.location_y - position.location_y) ** 2
        )

        if distance < self.acceptance_radius:
            if self.cycles_at_target < self.settling_threshold:
                self.cycles_at_target += 1
                return False
            return True

        self.cycles_at_target = 0
        return False
