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
        self._has_set_destination = False
        self._has_landed = False

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

        # Do something based on the report and the state of this class...
        status = report.status
        current_pos = report.position
        waypoint_pos = self.waypoint

        dist_x = waypoint_pos.location_x - current_pos.location_x
        dist_y = waypoint_pos.location_y - current_pos.location_y
        distance_to_waypoint = dist_x**2 + dist_y**2

        if status == drone_status.DroneStatus.LANDED:
            return command

        if distance_to_waypoint <= self.acceptance_radius**2:
            if status == drone_status.DroneStatus.HALTED and not self._has_landed:
                command = commands.Command.create_land_command()
                self._has_landed = True
            elif status != drone_status.DroneStatus.HALTED:
                command = commands.Command.create_halt_command()
            return command

        if not self._has_set_destination:
            if status == drone_status.DroneStatus.HALTED:
                new_x = dist_x
                new_y = dist_y

                if not (-60.0 <= new_x <= 60.0 and -60.0 <= new_y <= 60.0):
                    pass
                command = commands.Command.create_set_relative_destination_command(new_x, new_y)
                self._has_set_destination = True
        else:
            if distance_to_waypoint > self.acceptance_radius**2:
                if status == drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_set_relative_destination_command(new_x, new_y)
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
