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

        self.sent_initial_command = False  # Track if we've sent the first move command

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

        current = report.position

        # distance calculation
        distance_sq = (self.waypoint.location_x - current.location_x) ** 2 + (
            self.waypoint.location_y - current.location_y
        ) ** 2

        # if distance_sq <= self.acceptance_radius ** 2:

        # landed state
        # if report.status == drone_status.DroneStatus.LANDED:
        #    return command

        # halted state
        if report.status == drone_status.DroneStatus.HALTED:
            if distance_sq <= self.acceptance_radius**2:
                command = commands.Command.create_land_command()
            elif not self.sent_initial_command:  # only send move command once
                rel_x = self.waypoint.location_x - current.location_x
                rel_y = self.waypoint.location_y - current.location_y

                # Boundary check
                new_x = current.location_x + rel_x
                new_y = current.location_y + rel_y
                if -60 <= new_x <= 60 and -60 <= new_y <= 60:
                    command = commands.Command.create_set_relative_destination_command(rel_x, rel_y)
                    self.sent_initial_command = True

        # moving state
        elif report.status == drone_status.DroneStatus.MOVING:
            if distance_sq <= self.acceptance_radius**2:
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
