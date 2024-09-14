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

        self.heading_to_landing_pad = False
        self.has_reached_landing_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def reached_waypoint(self, position_x: float, position_y: float) -> bool:
        """
        Check if the drone has reached the waypoint.
        """
        distance_squared = (self.waypoint.location_x - position_x) ** 2 + (
            self.waypoint.location_y - position_y
        ) ** 2
        return distance_squared <= self.acceptance_radius**2

    def reached_landing_pad(
        self, position_x: float, position_y: float, landing_pad: location.Location
    ) -> bool:
        """
        Calculate the distance between the drone and a landing pad.
        """
        distance_squared = (landing_pad.location_x - position_x) ** 2 + (
            landing_pad.location_y - position_y
        ) ** 2
        return distance_squared <= self.acceptance_radius**2

    def pick_nearest_landing_pad(
        self, position_x: float, position_y: float, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        """
        Pick the nearest landing pad.
        """
        closest_pad = None
        closest_pad_distance_squared = float("inf")

        for potential_pad in landing_pad_locations:
            potential_pad_distance_squared = (potential_pad.location_x - position_x) ** 2 + (
                potential_pad.location_y - position_y
            ) ** 2
            if potential_pad_distance_squared < closest_pad_distance_squared:
                closest_pad = potential_pad
                closest_pad_distance_squared = potential_pad_distance_squared

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

        if not self.heading_to_landing_pad:
            if self.reached_waypoint(report.position.location_x, report.position.location_y):
                # Head to landing pad
                self.heading_to_landing_pad = True
            else:
                # Move to w aypoint
                relative_x = self.waypoint.location_x - report.position.location_x
                relative_y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(
                    relative_x, relative_y
                )
        elif self.heading_to_landing_pad:
            self.has_reached_landing_pad = self.reached_landing_pad(
                report.position.location_x,
                report.position.location_y,
                self.pick_nearest_landing_pad(
                    report.position.location_x, report.position.location_y, landing_pad_locations
                ),
            )

            if self.has_reached_landing_pad:
                # Head to landing pad
                command = commands.Command.create_land_command()
            else:
                # Move to landing pad
                relative_x = (
                    self.pick_nearest_landing_pad(
                        report.position.location_x,
                        report.position.location_y,
                        landing_pad_locations,
                    ).location_x
                    - report.position.location_x
                )
                relative_y = (
                    self.pick_nearest_landing_pad(
                        report.position.location_x,
                        report.position.location_y,
                        landing_pad_locations,
                    ).location_y
                    - report.position.location_y
                )
                command = commands.Command.create_set_relative_destination_command(
                    relative_x, relative_y
                )
        else:
            pass

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
