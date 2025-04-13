"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
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
        Make the drone fly to the waypoint.

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
        waypoint = self.waypoint
        # Do something based on the report and the state of this class...
        if (current_position.location_x == 0) and (current_position.location_y == 0):
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
        elif self._reached(current_position, waypoint) and (
            report.status != drone_status.DroneStatus.HALTED
        ):
            command = commands.Command.create_halt_command()

        elif report.status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_land_command()
        else:
            command = commands.Command.create_null_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
