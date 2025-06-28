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
        self.acceptance_radius = acceptance_radius
        self.has_moved = False

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
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        current_position = report.position
        acceptance_radius_squared = self.acceptance_radius * self.acceptance_radius

        # Calculate squared distance to waypoint (avoiding expensive sqrt)
        dx = self.waypoint.location_x - current_position.location_x
        dy = self.waypoint.location_y - current_position.location_y
        distance_squared = dx * dx + dy * dy

        if report.status == drone_status.DroneStatus.HALTED:
            if distance_squared <= acceptance_radius_squared:
                # We're close enough to the waypoint, land the drone
                return commands.Command.create_land_command()
            if not self.has_moved:
                # We haven't moved yet, send the move command
                self.has_moved = True
                return commands.Command.create_set_relative_destination_command(dx, dy)

        # Return null command to advance the simulator
        return commands.Command.create_null_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
