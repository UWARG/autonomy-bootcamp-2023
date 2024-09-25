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

        if report.position.location_x == 0 and report.position.location_y == 0:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
        if (
            report.position.location_x == self.waypoint.location_x
            and report.position.location_y == self.waypoint.location_y
            and self.closest_point is None
        ):
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
        if (
            self.closest_point
            and report.position.location_x == self.closest_point.location_x
            and report.position.location_y == self.closest_point.location_y
        ):
            command = commands.Command.create_land_command()
        if self.closest_point:
            print(
                "Closest point set to: ",
                self.closest_point,
                "Equals",
                report.position.location_x == self.closest_point.location_x,
                "Equals y",
                report.position.location_y == self.closest_point.location_y,
            )
        print("report", report)
        print("Locations", landing_pad_locations)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
