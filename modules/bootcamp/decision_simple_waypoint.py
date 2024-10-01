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
        self.trg_x = 0
        self.trg_y = 0

        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(
                waypoint.location_x, waypoint.location_y
            )
        ]

        self.land_status = 0
        # self.has_land = False
        # self.counter = 0

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

        def square(x: float) -> float:
            return x * x

        def wrong_rel_pos(i: int) -> bool:  # returns true if the drone halts at wrong position
            if i < 0 or i >= len(self.commands):
                return False
            cmd = self.commands[i]
            if cmd.get_command_type() == commands.Command.CommandType.SET_RELATIVE_DESTINATION:
                pos_x = report.position.location_x
                pos_y = report.position.location_y
                return square(pos_x - self.trg_x) + square(pos_y - self.trg_y) > square(
                    self.acceptance_radius
                )
            return False

        # Do something based on the report and the state of this class...
        pos_x = report.position.location_x
        pos_y = report.position.location_y
        if report.status == drone_status.DroneStatus.HALTED:  # if command done
            if wrong_rel_pos(self.command_index - 1):  # repeat previous command
                command = commands.Command.create_set_relative_destination_command(
                    self.trg_x - pos_x, self.trg_y - pos_y
                )
            elif self.command_index < len(self.commands):  # next command
                print(f"cmd({self.command_index}) pos({report.position})")
                command = self.commands[self.command_index]
                if (
                    command.get_command_type()
                    == commands.Command.CommandType.SET_RELATIVE_DESTINATION
                ):  # update target position
                    cmd_x, cmd_y = command.get_relative_destination()
                    self.trg_x += cmd_x
                    self.trg_y += cmd_y
                self.command_index += 1
            elif self.land_status == 0:  # start landing
                command = commands.Command.create_land_command()
                self.land_status = 2

        # self.counter += 1

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
