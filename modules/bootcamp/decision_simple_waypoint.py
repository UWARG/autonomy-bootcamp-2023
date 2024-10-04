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

        self.has_sent_landing_command = False

        self.waypoint_reached = False

        self.counter = 0

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def is_close(x: float, y: float, target_x: float, target_y: float, tolerance: float) -> bool:
        """Determines if coordinate x,y, is within (euclidean distance) tolerence of coordinate target_x, target_y."""
        dist = pow(pow((x - target_x), 2) + pow((y - target_y), 2), 0.5)
        return dist < tolerance

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

        # Default command
        command = commands.Command.create_null_command()
        print(report.position)

        if report.status == drone_status.DroneStatus.HALTED and not self.waypoint_reached:
            print(f"Halted at: {report.position}")
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x,
                self.waypoint.location_y - report.position.location_y,
            )
            if self.is_close(
                report.position.location_x,
                report.position.location_y,
                self.waypoint.location_x,
                self.waypoint.location_y,
                self.acceptance_radius,
            ):
                self.waypoint_reached = True

        elif (
            report.status == drone_status.DroneStatus.HALTED
            and self.waypoint_reached
            and not self.has_sent_landing_command
        ):
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True
        self.counter += 1
        print(command)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
