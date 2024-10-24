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

        position = report.position
        waypoint = self.waypoint
        status = report.status

        distance_from_waypoint_x = waypoint.location_x - position.location_x
        distance_from_waypoint_y = waypoint.location_y - position.location_y

        if status == drone_status.DroneStatus.HALTED:
            if distance_from_waypoint_x <= self.acceptance_radius and distance_from_waypoint_y <= self.acceptance_radius:
                command = commands.Command.create_land_command()
                print('Landing...')
            elif abs(waypoint.location_x) <= 60 and abs(waypoint.location_y) <= 60:
                command = commands.Command.create_set_relative_destination_command(distance_from_waypoint_x, distance_from_waypoint_y)
        elif status == drone_status.DroneStatus.MOVING:
            if report.destination == report.position:
                command = commands.Command.create_halt_command()
                print('Drone is moving')

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
