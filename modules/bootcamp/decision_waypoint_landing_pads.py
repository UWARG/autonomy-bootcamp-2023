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

    @staticmethod
    def get_x_difference(initial: location.Location, final: location.Location) -> float:
        """
        Get the difference in x values from initial and final locations.
        """
        return final.location_x - initial.location_x

    @staticmethod
    def get_y_difference(initial: location.Location, final: location.Location) -> float:
        """
        Get the difference in y values from initial and final locations.
        """
        return final.location_y - initial.location_y

    @staticmethod
    def get_distance_squared(diff_x: float, diff_y: float) -> float:
        """
        Return the distance squared of two locations based on their difference in x and y values.
        """
        return diff_x**2 + diff_y**2

    def get_closest_landing_pad(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        """
        Return the closest landing pad based on all landing pad locations.
        """
        min_distance = float("inf")
        closest_landing_pad = None
        for landing_pad in landing_pad_locations:
            x_difference = self.get_x_difference(report.position, landing_pad)
            y_difference = self.get_y_difference(report.position, landing_pad)
            if self.get_distance_squared(x_difference, y_difference) < min_distance:
                min_distance = self.get_distance_squared(x_difference, y_difference)
                closest_landing_pad = landing_pad
        return closest_landing_pad

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

        if self.reached_waypoint:
            self.waypoint = self.get_closest_landing_pad(report, landing_pad_locations)

        x_difference = DecisionWaypointLandingPads.get_x_difference(report.position, self.waypoint)
        y_difference = DecisionWaypointLandingPads.get_y_difference(report.position, self.waypoint)

        # If self.waypoint is None (also handles the case when no landing pad is found) default null command is sent
        if (
            report.status
            in {drone_status.DroneStatus.MOVING, report.status == drone_status.DroneStatus.LANDED}
            or self.waypoint is None
        ):
            command = commands.Command.create_null_command()
        elif DecisionWaypointLandingPads.get_distance_squared(x_difference, y_difference) >= (
            self.acceptance_radius**2
        ):
            command = commands.Command.create_set_relative_destination_command(
                x_difference, y_difference
            )
        else:
            if not self.reached_waypoint:
                self.reached_waypoint = True
            else:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
