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

        self.closest_point = None

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

        def manhattan_dist(loc: location.Location) -> int:
            return abs(loc.location_x - self.waypoint.location_x) + abs(
                loc.location_y - self.waypoint.location_y
            )

        def within(loc1: location.Location, loc2: location.Location) -> bool:
            radius_squared = self.acceptance_radius**2
            return (loc1.location_x - loc2.location_x) ** 2 + (
                loc1.location_y - loc2.location_y
            ) ** 2 <= radius_squared

        if report.position.location_x == 0 and report.position.location_y == 0:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )

        if self.closest_point is None and within(report.position, self.waypoint):
            dist = manhattan_dist(landing_pad_locations[0])
            loc = landing_pad_locations[0]
            for i in range(1, len(landing_pad_locations)):
                new_dist = manhattan_dist(landing_pad_locations[i])
                if new_dist < dist:
                    dist = new_dist
                    loc = landing_pad_locations[i]
            command = commands.Command.create_set_relative_destination_command(
                loc.location_x - self.waypoint.location_x, loc.location_y - self.waypoint.location_y
            )
            self.closest_point = loc

        if self.closest_point and within(report.position, self.closest_point):
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
