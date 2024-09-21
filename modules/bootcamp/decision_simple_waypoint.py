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

        self.waypoint_found = False
        self.landing_pad_found = False

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
        status = report.status
        current_position = report.position
        waypoint = self.waypoint

        relative_dest_x = waypoint.location_x - current_position.location_x
        relative_dest_y = waypoint.location_y - current_position.location_y
        distance_squared_to_waypoint = relative_dest_x**2 + relative_dest_y**2

        if status == drone_status.DroneStatus.HALTED:
            if distance_squared_to_waypoint < self.acceptance_radius**2:
                command = commands.Command.create_land_command()
                print("Drone is within range. Landing.")
            else:
                command = commands.Command.create_set_relative_destination_command(
                    relative_dest_x, relative_dest_y
                )
                print(f"Moving to waypoint: {waypoint.location_x}, {waypoint.location_y}")

        else:
            command = commands.Command.create_null_command()

        return command

    # Remove this when done
    # raise NotImplementedError

    # ============
    # BOOTCAMPERS MODIFY ABOVE THIS COMMENT
    # ============
