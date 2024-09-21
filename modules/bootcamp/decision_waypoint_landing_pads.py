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

        self.has_reached_waypoint = False
        self.closest_landing_pad = None

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

        if report.status == drone_status.DroneStatus.HALTED:
            allowed_error = self.acceptance_radius ** 2

            # Check if the landing pad or waypoint has already been reached
            if self.has_reached_waypoint:
                # Make sure the landing pad has actually been reached; otherwise send another set relative destination command
                if self.__squared_distance(report.position, self.closest_landing_pad) < allowed_error:
                    command = commands.Command.create_land_command()
                else:
                    relative_x = self.closest_landing_pad.location_x - report.position.location_x
                    relative_y = self.closest_landing_pad.location_y - report.position.location_y

                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )
            elif self.__squared_distance(report.position, self.waypoint) < allowed_error:
                self.closest_landing_pad = min(
                    landing_pad_locations,
                    key=lambda pad: self.__squared_distance(report.position, pad),
                )

                # Calculate relative x and y distance required to reach landing pad
                relative_x = self.closest_landing_pad.location_x - report.position.location_x
                relative_y = self.closest_landing_pad.location_y - report.position.location_y

                command = commands.Command.create_set_relative_destination_command(
                    relative_x, relative_y
                )

                self.has_reached_waypoint = True
            else:
                # Calculate relative x and y distance required to reach waypoint
                relative_x = self.waypoint.location_x - report.position.location_x
                relative_y = self.waypoint.location_y - report.position.location_y

                command = commands.Command.create_set_relative_destination_command(
                    relative_x, relative_y
                )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def __squared_distance(
        self, location1: location.Location, location2: location.Location
    ) -> float:
        """
        Calculate the distance between two Location objects.
        """

        return ((location2.location_x - location1.location_x) ** 2) + (
            (location2.location_y - location1.location_y) ** 2
        )
