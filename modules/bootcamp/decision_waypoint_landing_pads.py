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

        self.reached_at_waypoint = False
        self.reached_at_landing_pad = False

        self.the_closest_landing_pad = None
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
        command = commands.Command.create_null_command()
        status = report.status
        halted = drone_status.DroneStatus.HALTED

        if status == halted:
            if not self.reached_at_waypoint:
                waypoint_relative_x = self.waypoint.location_x - report.position.location_x
                waypoint_relative_y = self.waypoint.location_y - report.position.location_y

                if self.within_acceptance_radius(waypoint_relative_x, waypoint_relative_y):
                    self.reached_at_waypoint = True
                    self.the_closest_landing_pad = self.find_closest_landing_pad(
                        report.position, landing_pad_locations
                    )
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        waypoint_relative_x, waypoint_relative_y
                    )
            elif not self.reached_at_landing_pad:
                landing_pad_relative_x = (
                    self.the_closest_landing_pad.location_x - report.position.location_x
                )
                landing_pad_relative_y = (
                    self.the_closest_landing_pad.location_y - report.position.location_y
                )

                if self.within_acceptance_radius(landing_pad_relative_x, landing_pad_relative_y):
                    self.reached_at_landing_pad = True
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        landing_pad_relative_x, landing_pad_relative_y
                    )

        return command

    def within_acceptance_radius(self, dx: float, dy: float) -> bool:
        """
        Checks if its within the acceptance radius using Euclidean distance
        """
        return ((dx**2 + dy**2) ** 0.5) < self.acceptance_radius

    def find_closest_landing_pad(
        self, current_position: location.Location, landing_pads: "list[location.Location]"
    ) -> location.Location:
        """
        Finds the closest landing pad to the reference location.
        """
        closest_pad = None
        min_distance_squared = float("inf")
        for pad in landing_pads:
            dx = pad.location_x - current_position.location_x
            dy = pad.location_y - current_position.location_y
            distance_squared = dx**2 + dy**2
            if distance_squared < min_distance_squared:
                min_distance_squared = distance_squared
                closest_pad = pad
        return closest_pad
