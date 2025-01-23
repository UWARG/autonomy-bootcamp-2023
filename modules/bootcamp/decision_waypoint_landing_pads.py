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
        self.reached_landing_pad = False
        self.landing_pad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def find_distance_sqr(
        self, report: drone_report.DroneReport, other: location.Location
    ) -> float:
        """Finds the distance squared between the drone and an inputted location."""
        x_distance = report.position.location_x - other.location_x
        y_distance = report.position.location_y - other.location_y

        return x_distance**2 + y_distance**2

    def set_closest_landing_pad_location(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> None:
        """Sets the landing pad location to the nearest landing to the drone's current location."""
        self.landing_pad = landing_pad_locations[0]
        for landing_pad in landing_pad_locations:
            if self.find_distance_sqr(report, landing_pad) < self.find_distance_sqr(
                report, self.landing_pad
            ):
                self.landing_pad = landing_pad

    def reached_destination(
        self, report: drone_report.DroneReport, other: location.Location
    ) -> bool:
        """Checks if the drone has reached the inputted destination."""
        return self.find_distance_sqr(report, other) < self.acceptance_radius**2

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
            if not self.reached_waypoint:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x, self.waypoint.location_y
                )
            elif not self.reached_landing_pad:
                self.set_closest_landing_pad_location(report, landing_pad_locations)

                landing_pad_relative_x = self.landing_pad.location_x - report.position.location_x
                landing_pad_relative_y = self.landing_pad.location_y - report.position.location_y

                command = commands.Command.create_set_relative_destination_command(
                    landing_pad_relative_x, landing_pad_relative_y
                )
            else:
                command = commands.Command.create_land_command()

        if not self.reached_waypoint:
            if self.reached_destination(report, self.waypoint):
                self.reached_waypoint = True
                command = commands.Command.create_halt_command()
        elif not self.reached_landing_pad:
            if self.reached_destination(report, self.landing_pad):
                self.reached_landing_pad = True
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
