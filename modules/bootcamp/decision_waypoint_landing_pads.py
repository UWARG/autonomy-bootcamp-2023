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


def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculates the distance between two given points
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance


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

        self.__destination_type = ""

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

        distance_from_waypoint = calculate_distance(
            report.position.location_x,
            report.position.location_y,
            self.waypoint.location_x,
            self.waypoint.location_y,
        )
        if self.__destination_type == "landing_pad":
            distance_from_pad = calculate_distance(
                report.position.location_x,
                report.position.location_y,
                report.destination.location_x,
                report.destination.location_y,
            )
            if report.status.value == 1:
                command = commands.Command.create_land_command()
            elif distance_from_pad < self.acceptance_radius:
                command = commands.Command.create_halt_command()

        elif distance_from_waypoint < self.acceptance_radius:
            if report.status.value == 1:
                min_distance = float("inf")
                closest_pad = None
                for l in landing_pad_locations:
                    x1, y1 = report.position.location_x, report.position.location_y
                    x2, y2 = l.location_x, l.location_y
                    distance = calculate_distance(x1, y1, x2, y2)
                    if distance < min_distance:
                        min_distance = distance
                        closest_pad = location.Location(x2, y2)

                command = commands.Command.create_set_relative_destination_command(
                    closest_pad.location_x - report.position.location_x,
                    closest_pad.location_y - report.position.location_y,
                )
                self.__destination_type = "landing_pad"

            else:
                command = commands.Command.create_halt_command()
        elif report.status.value == 1:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
            self.__destination_type = "waypoint"

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
