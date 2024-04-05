"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Example decision with figure 8.
"""

from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionExample(base_decision.BaseDecision):
    """
    Example of sending commands to the drone.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(50.0, 37.5),
            commands.Command.create_set_relative_destination_command(0.0, -75.0),
            commands.Command.create_set_relative_destination_command(-50.0, 37.5),
            commands.Command.create_set_relative_destination_command(-50.0, -37.5),
            commands.Command.create_set_relative_destination_command(0.0, 75.0),
            commands.Command.create_set_relative_destination_command(50.0, -37.5),
            commands.Command.create_set_relative_destination_command(-50.0, 0.0),
            commands.Command.create_set_relative_destination_command(50.0, 0.0),
        ]

        self.has_sent_landing_command = False

        self.counter = 0

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
    ) -> commands.Command:
        """
        Makes the drone fly in a figure 8, then land.

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

        if (
            report.status == drone_status.DroneStatus.HALTED
            and self.command_index < len(self.commands)
        ):
            # Print some information for debugging
            print(self.counter)
            print(self.command_index)
            print("Halted at: " + str(report.position))

            command = self.commands[self.command_index]
            self.command_index += 1
        elif (
            report.status == drone_status.DroneStatus.HALTED
            and not self.has_sent_landing_command
        ):
            command = commands.Command.create_land_command()

            self.has_sent_landing_command = True

        self.counter += 1

        return command
