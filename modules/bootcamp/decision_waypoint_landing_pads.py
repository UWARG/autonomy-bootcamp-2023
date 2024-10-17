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

        self.drone_status = None
        self.waypoint_reached = False
        self.pause = False

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
        # define a functin to calculate distance between each item in an array and the current location
        def closest_landing_pad(
            report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
        ) -> location.Location:
            nearest_landing_pad = None
            nearest_distance_squared = float("inf")
            for landing_pad in landing_pad_locations:
                distance_squared = (report.position.location_x - landing_pad.location_x) ** 2 + (
                    report.position.location_y - landing_pad.location_y
                ) ** 2
                if distance_squared < nearest_distance_squared:
                    nearest_distance_squared = distance_squared
                    nearest_landing_pad = landing_pad
            return nearest_landing_pad

        while self.pause is True:
            return command
        if report.status == drone_status.DroneStatus.HALTED and self.waypoint_reached is False:
            radius_away_squared = (report.position.location_x - self.waypoint.location_x) ** 2 + (
                report.position.location_y - self.waypoint.location_y
            ) ** 2
            if radius_away_squared > self.acceptance_radius**2:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
            elif radius_away_squared <= self.acceptance_radius**2:
                self.waypoint_reached = True
        elif report.status == drone_status.DroneStatus.HALTED and self.waypoint_reached is True:
            nearest_landing_pad = closest_landing_pad(report, landing_pad_locations)
            command = commands.Command.create_set_relative_destination_command(
                nearest_landing_pad.location_x - report.position.location_x,
                nearest_landing_pad.location_y - report.position.location_y,
            )
            if (report.position.location_x - nearest_landing_pad.location_x) ** 2 + (
                report.position.location_y - nearest_landing_pad.location_y
            ) ** 2 <= self.acceptance_radius**2:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
