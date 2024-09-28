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

        self.command_index = 0
        self.commands = []
        self.counter = 0
        self.has_sent_landing_command = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def set_directions(self, report: drone_report.DroneReport) -> None:
        """ "
        set_directions and append it to the list
        """
        self.commands = []
        x_direction = self.waypoint.location_x - report.position.location_x
        y_direction = self.waypoint.location_y - report.position.location_y

        overbound = True
        while overbound:
            x_temp = x_direction
            y_temp = y_direction
            overbound = False
            if abs(x_direction) > 60:
                overbound = True
                if x_direction < 0:
                    x_temp = -60.0
                    x_direction += -60.0
                else:
                    x_temp = 60.0
                    x_direction += 60.0
            if abs(y_direction) > 60:
                overbound = True
                if y_direction < 0:
                    y_temp = -60.0
                    y_direction += -60.0
                else:
                    y_temp = 60.0
                    y_direction += 60.0

        self.commands.append(
            commands.Command.create_set_relative_destination_command(x_temp, y_temp)
        )

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

        if len(self.commands) == 0:
            self.set_directions(report)

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(
            self.commands
        ):

            print(self.counter)
            print(self.command_index)
            print(report.status)

            command = self.commands[self.command_index]
            self.command_index += 1

        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:

            if (
                abs(report.position.location_x - self.waypoint.location_x) > self.acceptance_radius
                and abs(report.position.location_y - self.waypoint.location_y)
                > self.acceptance_radius
            ):
                self.set_directions(report)
                self.command_index = 0
                command = self.commands[0]

            else:
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True

        self.counter += 1
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
