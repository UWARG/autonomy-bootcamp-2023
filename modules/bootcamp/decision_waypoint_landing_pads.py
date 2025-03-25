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
        # Flags to track status
        self.waypoint_reached = False
        self.acceptance_radius_squared = self.acceptance_radius**2
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
        if self.waypoint_reached:
            closest_landing_pad = None
            min_distance = float("inf")
            for landing_pad in landing_pad_locations:
                dx = report.position.location_x - landing_pad.location_x
                dy = report.position.location_y - landing_pad.location_y
                distance_squared = dx**2 + dy**2
                if distance_squared < min_distance:
                    min_distance = distance_squared
                    closest_landing_pad = landing_pad
            self.waypoint = closest_landing_pad
        dx = self.waypoint.location_x - report.position.location_x
        dy = self.waypoint.location_y - report.position.location_y
        distance_squared = dx**2 + dy**2
        if report.status in {drone_status.DroneStatus.MOVING, drone_status.DroneStatus.LANDED}:
            return command
        if distance_squared >= self.acceptance_radius_squared:
            command = commands.Command.create_set_relative_destination_command(dx, dy)
        else:
            if not self.waypoint_reached:
                self.waypoint_reached = True
            else:
                command = commands.Command.create_land_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
