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
        self.target_x = 0
        self.target_y = 0

        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(
                waypoint.location_x, waypoint.location_y
            )
        ]

        self.land_status = 0

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

        # python -m modules.bootcamp.tests.run_decision_simple_waypoint

        def wrong_rel_pos(i: int) -> bool:  # returns true if the drone halts at wrong position
            if i < 0 or i >= len(self.commands):
                return False
            cmd = self.commands[i]
            if cmd.get_command_type() == commands.Command.CommandType.SET_RELATIVE_DESTINATION:
                pos_x = report.position.location_x
                pos_y = report.position.location_y
                return (pos_x - self.target_x) ** 2 + (pos_y - self.target_y) ** 2 > (
                    self.acceptance_radius
                ) ** 2
            return False

        # Do something based on the report and the state of this class...
        pos_x = report.position.location_x
        pos_y = report.position.location_y
        if report.status == drone_status.DroneStatus.HALTED:  # if command done
            if self.command_index < len(self.commands):  # next command
                print(f"cmd({self.command_index}) pos({report.position})")
                command = self.commands[self.command_index]
                if (
                    command.get_command_type()
                    == commands.Command.CommandType.SET_RELATIVE_DESTINATION
                ):  # update target position
                    self.target_x = self.waypoint.location_x
                    self.target_y = self.waypoint.location_y
                self.command_index += 1
            elif wrong_rel_pos(self.command_index - 1):  # repeat previous command
                command = commands.Command.create_set_relative_destination_command(
                    self.target_x - pos_x, self.target_y - pos_y
                )
            elif self.land_status == 0:  # start landing
                command = commands.Command.create_land_command()
                self.land_status = 2

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
