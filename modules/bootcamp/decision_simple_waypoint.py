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

        self.exited = False

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

        x_dist = self.waypoint.location_x - report.position.location_x
        y_dist = self.waypoint.location_y - report.position.location_y
        dist = (x_dist * x_dist + y_dist * y_dist) ** 0.5

        if report.status == drone_status.DroneStatus.HALTED and dist > self.acceptance_radius:
            # we are currently stopped so check the next closest waypoint to our destination
            x_delta = min(max(-60, x_dist), 60)
            y_delta = min(max(-60, y_dist), 60)
            command = commands.Command.create_set_relative_destination_command(x_delta, y_delta)
            # command = commands.command.create_set_relative_destination_command(x_delta, y_delta)

        if dist <= self.acceptance_radius and not self.exited:
            command = commands.Command.create_land_command()
            # self.exited = true
            return command

        print("Info: ", x_dist, y_dist, dist)

        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
