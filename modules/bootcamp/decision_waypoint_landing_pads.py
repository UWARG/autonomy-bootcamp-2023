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

        def distance_sqr(position: location.Location, destination: location.Location) -> float:
            pos_x = position.location_x
            pos_y = position.location_y
            des_x = destination.location_x
            des_y = destination.location_y

            return (pos_x - des_x) ** 2 + (pos_y - des_y) ** 2

        def in_radius(
            position: location.Location, destination: location.Location, radius: float
        ) -> bool:
            distance = distance_sqr(position, destination)

            return distance < radius**2

        def closest_landing_pad(
            landing_pad_locations: "list[location.Location]", waypoint: location.Location
        ) -> location.Location:

            closest_lp = None
            min_distance = float("inf")

            for lp in landing_pad_locations:
                distance = distance_sqr(lp, waypoint)
                if distance < min_distance:
                    min_distance = distance
                    closest_lp = lp
            return closest_lp

        if self.reached_waypoint is False:
            if in_radius(report.position, self.waypoint, self.acceptance_radius):
                self.reached_waypoint = True
                command = commands.Command.create_halt_command()
            else:
                dx = self.waypoint.location_x - report.position.location_x
                dy = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(dx, dy)

        else:
            closest_lp = closest_landing_pad(landing_pad_locations, self.waypoint)
            if in_radius(report.position, closest_lp, self.acceptance_radius):
                if report.status == drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_halt_command()
            else:
                dx = closest_lp.location_x - report.position.location_x
                dy = closest_lp.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(dx, dy)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
