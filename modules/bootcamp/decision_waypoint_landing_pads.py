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

        print(str(waypoint.location_x) + ", " + str(waypoint.location_y))

        # assuming this is to give destinations n stuff
        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(
                waypoint.location_x, waypoint.location_y
            ),
            # commands.Command.create_set_relative_destination_command(1.0, 1.0),
        ]

        self.has_sent_landing_command = False

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

        # Default command
        command = commands.Command.create_null_command()

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(
            self.commands
        ):
            # Print some information for debugging
            print("Landing Pad Locations:")

            print(self.counter)
            print(self.command_index)
            print("Halted at: " + str(report.position))

            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:

            # stuff when landed @ waypoint
            closest_location = None
            min_distance_sq = float("inf")

            for pad_location in landing_pad_locations:
                print("report position: " + str(report.position))
                print(str(pad_location))

                # no square root!
                distance_sq = (report.position.location_x - pad_location.location_x) ** 2 + (
                    report.position.location_y - pad_location.location_y
                ) ** 2

                if distance_sq < min_distance_sq:
                    min_distance_sq = distance_sq
                    closest_location = pad_location

            if closest_location is not None:
                command = commands.Command.create_set_relative_destination_command(
                    closest_location.location_x - report.position.location_x,
                    closest_location.location_y - report.position.location_y,
                )

            self.has_sent_landing_command = True
        elif self.has_sent_landing_command:
            command = commands.Command.create_land_command()
        # works!!

        self.counter += 1

        return command

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
