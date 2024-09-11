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

        self.has_sent_landing_command = False
        self.mission_completed = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    def clearance(self, report: drone_report.DroneReport) -> bool:
        """Function checks whether the drone has reached waypoint without using square root operation"""
        distance_x = self.waypoint.location_x - report.position.location_x
        distance_y = self.waypoint.location_y - report.position.location_y
        distance_squared = distance_x**2 + distance_y**2
        clear = distance_squared < self.acceptance_radius**2
        return clear

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



        if report.status == drone_status.DroneStatus.HALTED:
            if not self.clearance(report):
                print(f"Departed for waypoint mission from halted position : {report.position}")
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x-report.position.location_x, self.waypoint.location_y-report.position.location_y)
            elif not self.has_sent_landing_command:
                print("send landing command")
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True
        elif report.status == drone_status.DroneStatus.MOVING and self.clearance(report):
            command = commands.Command.create_halt_command()
            print("HALT COMMAND SENT")



        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
