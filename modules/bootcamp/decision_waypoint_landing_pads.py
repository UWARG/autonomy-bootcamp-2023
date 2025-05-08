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

        # Add your own
        self.closest_from_landing = 999999999
        self.closest_landing_x = 999999999
        self.closest_landing_y = 999999999
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
        waypoint_dx = self.waypoint.location_x - report.position.location_x
        waypoint_dy = self.waypoint.location_y - report.position.location_y
        dist_from_accept = (waypoint_dx * waypoint_dx + waypoint_dy * waypoint_dy) ** (
            1.0 / 2.0
        ) - self.acceptance_radius

        landing_dx = self.closest_landing_x - report.position.location_x
        landing_dy = self.closest_landing_y - report.position.location_y
        dist_from_landing = (landing_dx * landing_dx + landing_dy * landing_dy) ** (
            1.0 / 2.0
        ) - self.acceptance_radius
        # Do something based on the report and the state of this class...
        if report.status.name == "HALTED" and dist_from_landing > 0:
            if dist_from_accept > 0:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
            else:
                for loc in landing_pad_locations:
                    current_from_landing = loc.location_x**2 + loc.location_y**2
                    if current_from_landing < self.closest_from_landing:
                        self.closest_from_landing = current_from_landing
                        self.closest_landing_x = loc.location_x
                        self.closest_landing_y = loc.location_y
                command = commands.Command.create_set_relative_destination_command(
                    self.closest_landing_x - report.position.location_x,
                    self.closest_landing_y - report.position.location_y,
                )
        elif report.status.name == "HALTED":
            command = commands.Command.create_land_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
