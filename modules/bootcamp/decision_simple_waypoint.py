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

        # Track if we've attempted to move to handle edge cases
        self.movement_attempted = False

        # Store last position to detect if we're actually moving
        self.last_position = None

        # Count consecutive stationary updates to detect if stuck
        self.stationary_count = 0

    def _calculate_squared_distance(
        self, pos1: location.Location, pos2: location.Location
    ) -> float:
        """
        Calculate the squared Euclidean distance between two locations.
        """
        return (pos1.location_x - pos2.location_x) ** 2 + (pos1.location_y - pos2.location_y) ** 2

    def _is_stationary(self, report: drone_report.DroneReport) -> bool:
        """
        Check if drone hasn't moved significantly since last update.
        """
        if report.status == drone_status.DroneStatus.HALTED:
            return True  # If the drone is halted, it's stationary.

        if self.last_position is None:
            self.last_position = report.position
            return True

        # Check if the drone hasn't moved significantly
        is_stationary = (
            self._calculate_squared_distance(report.position, self.last_position) < 0.000001
        )
        self.last_position = report.position
        return is_stationary

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

        sqr_distance_to_waypoint = self._calculate_squared_distance(report.position, self.waypoint)

        # Check if we're initially halted
        if self._is_stationary(report):
            self.stationary_count += 1
        else:
            self.stationary_count = 0

        # If we're within acceptance radius, land
        if sqr_distance_to_waypoint <= self.acceptance_radius**2:
            if report.status == drone_status.DroneStatus.HALTED:
                return commands.Command.create_land_command()

            return commands.Command.create_halt_command()

        # If halted, either from start or mid-flight
        if report.status == drone_status.DroneStatus.HALTED:
            # Calculate relative movement needed
            dx = self.waypoint.location_x - report.position.location_x
            dy = self.waypoint.location_y - report.position.location_y
            self.movement_attempted = True
            return commands.Command.create_set_relative_destination_command(dx, dy)

        # If we're stuck or outside boundaries, halt
        if self.stationary_count > 5:
            return commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
