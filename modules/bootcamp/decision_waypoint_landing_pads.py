"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
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


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
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

        self.reached_waypoint = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

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

        if not self.reached_waypoint:
            dx = self.waypoint.location_x - report.position.location_x
            dy = self.waypoint.location_y - report.position.location_y
            squared_distance_to_waypoint = dx**2 + dy**2
            if squared_distance_to_waypoint < self.acceptance_radius**2:
                self.reached_waypoint = True
                command = commands.Command.create_halt_command()
            else:
                command = commands.Command.create_set_relative_destination_command(dx, dy)
        else:
            closest_pad = min(
                landing_pad_locations,
                key=lambda pad: (pad.location_x - self.waypoint.location_x) ** 2
                + (pad.location_y - self.waypoint.location_y) ** 2,
            )
            dx = closest_pad.location_x - report.position.location_x
            dy = closest_pad.location_y - report.position.location_y
            squared_distance_to_pad = dx**2 + dy**2
            if squared_distance_to_pad < self.acceptance_radius**2:
                if report.status == drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_halt_command()
            else:
                command = commands.Command.create_set_relative_destination_command(dx, dy)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
