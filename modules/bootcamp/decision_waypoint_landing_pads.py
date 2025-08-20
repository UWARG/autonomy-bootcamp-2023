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

        # Track which stage of the mission we're in
        self.at_waypoint = False
        self.closest_landing_pad = None
        self.at_landing_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def _calculate_squared_distance(
        self, location1: location.Location, location2: location.Location
    ) -> float:
        """
        Calculate distance between two locations.
        """
        dx = location1.location_x - location2.location_x
        dy = location1.location_y - location2.location_y
        distance_squared = dx**2 + dy**2
        return distance_squared

    def _find_closest_landing_pad(
        self, landing_pad_locations: "list[location.Location]"
    ) -> "location.Location | None":
        """
        Find the landing pad closest to the waypoint.
        """
        if not landing_pad_locations:
            return None

        closest_pad = None
        closest_distance_squared = float("inf")  # Start with infinity

        for pad in landing_pad_locations:
            distance_squared = self._calculate_squared_distance(self.waypoint, pad)
            if distance_squared < closest_distance_squared:
                closest_distance_squared = distance_squared
                closest_pad = pad

        return closest_pad

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
            if not self.at_waypoint:
                relative_x = self.waypoint.location_x - report.position.location_x
                relative_y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(
                    relative_x, relative_y
                )
            elif self.at_waypoint and self.closest_landing_pad is None:
                self.closest_landing_pad = self._find_closest_landing_pad(landing_pad_locations)
                if self.closest_landing_pad:
                    print(f"Found closest landing pad at: {self.closest_landing_pad}")
            elif self.closest_landing_pad and not self.at_landing_pad:
                relative_x = self.closest_landing_pad.location_x - report.position.location_x
                relative_y = self.closest_landing_pad.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(
                    relative_x, relative_y
                )
            elif self.at_landing_pad:
                command = commands.Command.create_land_command()
                print("Landing on the landing pad!")

        if not self.at_waypoint:
            distance_to_waypoint_squared = self._calculate_squared_distance(
                report.position, self.waypoint
            )

            if distance_to_waypoint_squared <= self.acceptance_radius**2:
                self.at_waypoint = True
                print("Reached waypoint! Now searching for landing pads...")

        elif self.closest_landing_pad and not self.at_landing_pad:
            distance_to_pad_squared = self._calculate_squared_distance(
                report.position, self.closest_landing_pad
            )

            if distance_to_pad_squared <= self.acceptance_radius**2:
                self.at_landing_pad = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
