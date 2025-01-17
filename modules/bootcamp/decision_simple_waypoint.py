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

        current_position = report.position
        drone_status_value = report.status

        distance_to_waypoint = pow(pow(self.waypoint.location_x - current_position.location_x, 2) + pow(self.waypoint.location_y - current_position.location_y, 2), 0.5)

        if drone_status_value == drone_status.DroneStatus.HALTED and distance_to_waypoint <= self.acceptance_radius:
            return commands.Command.create_land_command()
        
        elif drone_status_value == drone_status.DroneStatus.HALTED and distance_to_waypoint > self.acceptance_radius:
            relative_x = self.waypoint.location_x - current_position.location_x
            relative_y = self.waypoint.location_y - current_position.location_y
            new_x = current_position.location_x + relative_x
            new_y = current_position.location_y + relative_y
            if -60.0 <= new_x <= 60.0 and -60.0 <= new_y <= 60.0:
                return commands.Command.create_set_relative_destination_command(relative_x, relative_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
