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

        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(
                waypoint.location_x, waypoint.location_y
            )
        ]
        self.has_sent_landing_command = False
        self.has_reached_waypoint = False
        self.has_caculated_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def closest_pad(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> int:
        """ "
        Finds the index of the closest pad
        """
        _min = -1.0
        closest_index = 0
        index = 0

        for loc in landing_pad_locations:
            print(f"landing pad locations: {landing_pad_locations}")
            print(f"location being evaluated: {loc}")
            x_distance = loc.location_x - report.position.location_x
            y_distance = loc.location_y - report.position.location_y
            if x_distance**2 + y_distance**2 < _min or _min == -1.0:
                closest_index = index
                _min = x_distance**2 + y_distance**2
            index += 1

        if _min <= self.acceptance_radius:
            return -1

        return closest_index

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

        if report.status == drone_status.DroneStatus.HALTED and self.has_reached_waypoint:

            if not self.has_caculated_pad:
                closest_index = self.closest_pad(report, landing_pad_locations)

                if closest_index != -1:
                    self.commands.append(
                        commands.Command.create_set_relative_destination_command(
                            landing_pad_locations[closest_index].location_x
                            - report.position.location_x,
                            landing_pad_locations[closest_index].location_y
                            - report.position.location_y,
                        )
                    )

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(
            self.commands
        ):

            print(self.command_index)
            print(report.status)

            command = self.commands[self.command_index]
            self.command_index += 1

            if self.command_index == len(self.commands):
                self.has_reached_waypoint = True

        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            command = commands.Command.create_land_command()

            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
