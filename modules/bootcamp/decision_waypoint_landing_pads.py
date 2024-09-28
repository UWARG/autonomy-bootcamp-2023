"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
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


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
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
        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(
                waypoint.location_x, waypoint.location_y
            )
        ]

        self.has_goto_land = False
        self.has_land = False
        self.counter = 0

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

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
        pos_x = report.position.location_x
        pos_y = report.position.location_y
        if report.status == drone_status.DroneStatus.HALTED:  # if command done
            if self.command_index < len(self.commands):  # next command
                print(f"frame({self.counter}) cmd({self.command_index}) pos({report.position})")
                command = self.commands[self.command_index]
                self.command_index += 1
            elif not self.has_goto_land:  # go to landing
                min_dist = 1e18
                close_x = 0
                close_y = 0
                for landing_pad in landing_pad_locations:
                    land_x = landing_pad.location_x
                    land_y = landing_pad.location_y
                    dist = (pos_x - land_x) * (pos_x - land_x) + (pos_y - land_y) * (pos_y - land_y)
                    if dist < min_dist:
                        min_dist = dist
                        close_x = land_x
                        close_y = land_y
                command = commands.Command.create_set_relative_destination_command(
                    close_x - pos_x, close_y - pos_y
                )
                self.has_goto_land = True
            elif not self.has_land:  # start landing
                command = commands.Command.create_land_command()
                self.has_land = True

        self.counter += 1

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
