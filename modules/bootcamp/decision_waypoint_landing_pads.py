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

        # index to ensure only one command is sent: self.command
        # self.command_index = 0

        self.has_sent_landing_command = False

        self.find_nearest_landing_pad = False

        self.reached_waypoint = False

        # after reaching the waypoint, begin moving to landing pad
        # at this stage, you don't need to find way to waypoint anymore!
        self.moving_to_landing_pad = False

        self.counter = 0

    def at_waypoint(self, current_x: float, current_y: float) -> bool:
        """
        checks if the drone has reached the waypoint. Returns boolean
        """
        distance_squared = (self.waypoint.location_x - current_x) ** 2 + (
            self.waypoint.location_y - current_y
        ) ** 2
        return distance_squared <= self.acceptance_radius**2

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

        # if it isn't at the waypoint yet, it hasn't reached; so it moves around till it reaches the waypoint
        self.reached_waypoint = self.at_waypoint(
            report.position.location_x, report.position.location_y
        )

        if (
            report.status == drone_status.DroneStatus.HALTED
            and not self.reached_waypoint
            and not self.moving_to_landing_pad
        ):

            relative_x = self.waypoint.location_x - report.position.location_x
            relative_y = self.waypoint.location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(
                relative_x, relative_y
            )

        elif report.status == drone_status.DroneStatus.HALTED and self.reached_waypoint:

            # stuff when landed @ waypoint
            self.moving_to_landing_pad = True
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
            command = commands.Command.create_halt_command()
            command = commands.Command.create_land_command()
        # works!!

        self.counter += 1

        return command

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
