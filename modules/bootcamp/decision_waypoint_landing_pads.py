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

        self.waypoint_reached = False
        self.target_landing_pad = None

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

        def calc_sqr_dist(loc1: location.Location, loc2: location.Location) -> float:
            return (loc1.location_x - loc2.location_x) ** 2 + (
                loc1.location_y - loc2.location_y
            ) ** 2

        def find_closest_landing_pad(
            drone_location: location.Location, landing_pad_locations: "list[location.Location]"
        ) -> location.Location | None:
            """
            Find the closest landing pad to the drone's location.
            """
            closest_landing_pad = None
            min_distance = float("inf")

            for landing_pad in landing_pad_locations:
                distance = calc_sqr_dist(drone_location, landing_pad)
                if distance < min_distance:
                    min_distance = distance
                    closest_landing_pad = landing_pad

            return closest_landing_pad

        if report.status == drone_status.DroneStatus.HALTED:
            if (
                self.waypoint_reached
                and calc_sqr_dist(self.target_landing_pad, report.position)
                <= self.acceptance_radius**2
            ):
                # Landing at closest landing pad
                command = command.create_land_command()
            elif calc_sqr_dist(self.waypoint, report.position) <= self.acceptance_radius**2:
                # Arrived at waypoint, now find and go to closest landing pad
                self.waypoint_reached = True
                self.target_landing_pad = find_closest_landing_pad(
                    report.position, landing_pad_locations
                )

                if self.target_landing_pad is not None:
                    dx = self.target_landing_pad.location_x - report.position.location_x
                    dy = self.target_landing_pad.location_y - report.position.location_y
                    command = command.create_set_relative_destination_command(dx, dy)
                else:
                    # No landing pad available
                    command = command.create_null_command()
            else:
                command = command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
