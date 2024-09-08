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
        self.landed_at_waypoint = False

    def __get_distance(self, position_1: location.Location, position_2: location.Location) -> float:
        return (
            (position_1.location_x - position_2.location_x) ** 2
            + (position_1.location_y - position_2.location_y) ** 2
        ) ** 0.5

    def __get_closest_landing_pad(
        self, drone_location: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        print("getting closest...")

        minimum_distance = float("inf")
        closest_landing_pad_index = 0

        for i, landing_pad in enumerate(landing_pad_locations):
            distance = self.__get_distance(drone_location, landing_pad)

            if minimum_distance > distance:
                closest_landing_pad_index = i
                minimum_distance = distance

        return landing_pad_locations[closest_landing_pad_index]

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

        if self.waypoint == report.position:
            if self.landed_at_waypoint:
                command = commands.Command.create_land_command()

            self.landed_at_waypoint = True

            print("trying to find closest...")
            self.waypoint = self.__get_closest_landing_pad(report.position, landing_pad_locations)
        elif report.status == drone_status.DroneStatus.HALTED:
            relative_destination_x = self.waypoint.location_x - report.position.location_x
            relative_destination_y = self.waypoint.location_y - report.position.location_y

            command = commands.Command.create_set_relative_destination_command(
                relative_destination_x, relative_destination_y
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
