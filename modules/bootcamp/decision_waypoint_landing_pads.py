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

        self.command = commands.Command.create_set_relative_destination_command(
            waypoint.location_x, waypoint.location_y
        )

        self.has_begun = False
        self.has_reached_waypoint = False

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

        # halted at the beginning
        if report.status == drone_status.DroneStatus.HALTED and not self.has_begun:
            command = self.command
            self.has_begun = True

        # halted at the waypoint
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_reached_waypoint:
            # we now need to check for distances to landing pads, and choose which one is the best
            min_distance_squared = float("inf")
            best_landing_pad = -1
            # iterate through each landing pad
            for index, landing_pad in enumerate(landing_pad_locations):
                distance_squared = (landing_pad.location_x - self.waypoint.location_x) ** 2 + (
                    landing_pad.location_y - self.waypoint.location_y
                ) ** 2
                if distance_squared < min_distance_squared:
                    min_distance_squared = distance_squared
                    best_landing_pad = index

            # create a relative destination
            command = commands.Command.create_set_relative_destination_command(
                landing_pad_locations[best_landing_pad].location_x - self.waypoint.location_x,
                landing_pad_locations[best_landing_pad].location_y - self.waypoint.location_y,
            )
            self.has_reached_waypoint = True

        # halt at the landing pad
        elif report.status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
