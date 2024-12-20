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
        self.reached_waypoint = False  # Tracks if the waypoint has been reached
        self.closest_landing_pad = None  # Stores the closest landing pad
        self.has_sent_land_command = False  # Tracks if the land command has been sent
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

        # Do something based on the report and the state of this class...

        def distance_squared(loc1: location.Location, loc2: location.Location) -> float:
            """Calculate the squared Euclidean distance between two locations."""
            return (loc1.location_x - loc2.location_x) ** 2 + (
                loc1.location_y - loc2.location_y
            ) ** 2

        def within_radius(loc1: location.Location, loc2: location.Location, radius: float) -> bool:
            """Check if two locations are within the specified radius."""
            return distance_squared(loc1, loc2) <= radius**2

        # If the drone hasn't reached the waypoint, set it as the destination
        if not self.reached_waypoint:
            if within_radius(report.position, self.waypoint, self.acceptance_radius):
                self.reached_waypoint = True
                command = commands.Command.create_halt_command()
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )

        # If the waypoint has been reached, determine the closest landing pad
        elif self.closest_landing_pad is None:
            min_distance = float("inf")
            for pad in landing_pad_locations:
                dist = distance_squared(self.waypoint, pad)
                if dist < min_distance:
                    min_distance = dist
                    self.closest_landing_pad = pad

            if self.closest_landing_pad:
                command = commands.Command.create_set_relative_destination_command(
                    self.closest_landing_pad.location_x - report.position.location_x,
                    self.closest_landing_pad.location_y - report.position.location_y,
                )

        # If the drone is at the closest landing pad, issue the land command
        elif (
            self.closest_landing_pad
            and within_radius(report.position, self.closest_landing_pad, self.acceptance_radius)
            and not self.has_sent_land_command
        ):
            command = commands.Command.create_land_command()
            self.has_sent_land_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
