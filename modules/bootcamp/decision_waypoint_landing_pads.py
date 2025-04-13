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
        self.step = "START"
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def _distance(self, location1: location.Location, location2: location.Location) -> tuple:
        """
        Calculate the squared distance and differences between two locations.

        :param location1: First location
        :param location2: Second location
        :return: Tuple containing (squared_distance, x_difference, y_difference)
        """
        x_difference = location2.location_x - location1.location_x
        y_difference = location2.location_y - location1.location_y
        return (
            (x_difference * x_difference + y_difference * y_difference),
            x_difference,
            y_difference,
        )

    def _reached(
        self, current_position: location.Location, target_position: location.Location
    ) -> bool:
        """
        Check if the current position is within acceptance radius of the target.

        :param current_position: Current drone position
        :param target_position: Target position to check against
        :return: True if within acceptance radius, False otherwise
        """
        return self._distance(current_position, target_position)[0] <= (
            self.acceptance_radius * self.acceptance_radius
        )

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
        current_position = report.position
        min_distance = 28800
        x_distance = 0
        y_distance = 0
        closest_pad = None
        for pad in landing_pad_locations:
            distance = self._distance(self.waypoint, pad)
            if distance[0] < min_distance:
                min_distance = distance[0]
                x_distance = distance[1]
                y_distance = distance[2]
                closest_pad = pad

        if (report.status == drone_status.DroneStatus.HALTED) and (self.step == "START"):
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
            self.step = "WAYPOINT"
        elif (self.step == "WAYPOINT") and self._reached(current_position, self.waypoint):
            command = commands.Command.create_halt_command()
            self.step = "STOPPED_AT_WAYPOINT"
        elif (
            (self.step == "STOPPED_AT_WAYPOINT")
            and self._reached(current_position, self.waypoint)
            and (report.status == drone_status.DroneStatus.HALTED)
        ):
            command = commands.Command.create_set_relative_destination_command(
                x_distance, y_distance
            )
            self.step = "AT_PAD"
        elif (self.step == "AT_PAD") and self._reached(current_position, closest_pad):
            command = commands.Command.create_halt_command()
            self.step = "STOPPED_AT_PAD"
        elif (
            (self.step == "STOPPED_AT_PAD")
            and self._reached(current_position, closest_pad)
            and (report.status == drone_status.DroneStatus.HALTED)
        ):
            command = commands.Command.create_land_command()
            self.step = "LANDED"
        else:
            command = commands.Command.create_null_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
