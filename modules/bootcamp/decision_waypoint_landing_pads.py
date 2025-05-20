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
        self.is_at_waypoint = False
        self.nearest_landing = None
        self.landed = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def calculate_dist(self, position: location.Location, dest: location.Location) -> float:
        """
        Calculates if in acceptance radius
        """
        return (position.location_x - dest.location_x) ** 2 + (
            position.location_y - dest.location_y
        ) ** 2

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
        if not self.is_at_waypoint:
            if self.calculate_dist(report.position, self.waypoint) < self.acceptance_radius**2:
                command = commands.Command.create_halt_command()
                self.is_at_waypoint = True

            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )

        elif self.nearest_landing is None:
            shortest = float("inf")
            for landing_pads in landing_pad_locations:

                current = self.calculate_dist(report.position, landing_pads)
                if current < shortest:
                    shortest = current
                    self.nearest_landing = landing_pads
            command = commands.Command.create_set_relative_destination_command(
                self.nearest_landing.location_x - report.position.location_x,
                self.nearest_landing.location_y - report.position.location_y,
            )

        elif self.calculate_dist(report.position, self.nearest_landing) < self.acceptance_radius**2:
            command = commands.Command.create_land_command()
            self.landed = True

        else:
            command = commands.Command.create_set_relative_destination_command(
                self.nearest_landing.location_x - report.position.location_x,
                self.nearest_landing.location_y - report.position.location_y,
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
