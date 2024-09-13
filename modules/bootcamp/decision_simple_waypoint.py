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

    def relative_location_from_waypoint(self, current_x: float, current_y: float) -> float:
        """
        Finds how far you are from the waypoint based off your current location
        """
        waypoint_x, waypoint_y = self.waypoint.location_x, self.waypoint.location_y

        return (waypoint_x - current_x), (waypoint_y - current_y)

    def at_waypoint(self, current_x: float, current_y: float) -> bool:
        """
        Returns if you are at the waypoint or not
        """
        dist_to_waypoint = sum(
            dist**2 for dist in self.relative_location_from_waypoint(current_x, current_y)
        )
        if dist_to_waypoint**0.5 <= self.acceptance_radius:
            return True
        return False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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

        current_x, current_y = report.position.location_x, report.position.location_y

        if report.status == drone_status.DroneStatus.HALTED and self.at_waypoint(
            current_x, current_y
        ):
            command = commands.Command.create_land_command()

        elif report.status == drone_status.DroneStatus.HALTED and not self.at_waypoint(
            current_x, current_y
        ):
            relative_x_dist_to_waypoint, relative_y_dist_to_waypoint = (
                self.relative_location_from_waypoint(current_x, current_y)
            )
            command = commands.Command.create_set_relative_destination_command(
                relative_x_dist_to_waypoint, relative_y_dist_to_waypoint
            )

        else:
            print("Something goofed RIP")

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
