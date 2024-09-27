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
        self.reached_landpad = False

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

        if report.status == drone_status.DroneStatus.HALTED:
            x_dist = self.waypoint.location_x - report.position.location_x
            y_dist = self.waypoint.location_y - report.position.location_y
            if not self.within_range(report, self.waypoint) and not self.reached_waypoint:
                command = commands.Command.create_set_relative_destination_command(x_dist, y_dist)
            elif not self.reached_landpad:
                self.reached_waypoint = True
                nearest_pad = self.nearest_land_pad(self.waypoint, landing_pad_locations)
                if not self.within_range(report, nearest_pad):
                    x_pad = nearest_pad.location_x - report.position.location_x
                    y_pad = nearest_pad.location_y - report.position.location_y
                    command = commands.Command.create_set_relative_destination_command(x_pad, y_pad)
                else:
                    self.reached_landpad = True
            else:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def within_range(self, report: drone_report.DroneReport, waypoint: location.Location) -> bool:
        """
        Calculates how far the drone is from the waypoint in the x and y direction
        """
        x_dist = waypoint.location_x - report.position.location_x
        y_dist = waypoint.location_y - report.position.location_y

        if x_dist**2 + y_dist**2 <= self.acceptance_radius**2:
            return True
        return False

    def nearest_land_pad(
        self, waypoint: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        """
        Calculates the closest landing pad from the drone's location
        """
        min_dist = float("inf")
        min_pad = location.Location
        for pad in landing_pad_locations:
            x_dist = waypoint.location_x - pad.location_x
            y_dist = waypoint.location_y - pad.location_y
            curr_dist = x_dist**2 + y_dist**2
            if curr_dist < min_dist:
                min_dist = curr_dist
                min_pad = pad
        return min_pad
