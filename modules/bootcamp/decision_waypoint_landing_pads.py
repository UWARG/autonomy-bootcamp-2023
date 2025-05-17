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

        self.cycles_at_target = 0  # counts loops passed when drone is within accepted radius
        self.at_target_cycles = 5

        self.command_index = 0  # tracks which step of the sequence the drone is at

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

        if report.status == drone_status.DroneStatus.HALTED:
            match self.command_index:
                case 0:
                    if self.at_target(report.position, report.destination):
                        self.command_index += 1
                    else:
                        command = commands.Command.create_set_relative_destination_command(
                            self.waypoint.location_x - report.position.location_x,
                            self.waypoint.location_y - report.position.location_y,
                        )

                case 1:
                    closest_location = self.get_closest_pad(landing_pad_locations, report.position)

                    command = commands.Command.create_set_relative_destination_command(
                        closest_location.location_x - report.position.location_x,
                        closest_location.location_y - report.position.location_y,
                    )

                    if self.at_target(report.position, report.destination):
                        self.command_index += 1

                case 2:
                    command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def at_target(self, position: location.Location, target: location.Location) -> bool:
        """
        returns if position has been within target for certain amount of loops
        """
        distance = self.get_squared_distance(position, target)
        if distance < self.acceptance_radius**2:
            if self.cycles_at_target < self.at_target_cycles:
                self.cycles_at_target += 1
                return False

            return True

        self.cycles_at_target = 0
        return False

    def get_squared_distance(self, position: location.Location, target: location.Location) -> float:
        """
        returns the distance between two points squared
        """
        sqr_distance = (target.location_x - position.location_x) ** 2 + (
            target.location_y - position.location_y
        ) ** 2
        return sqr_distance

    def get_closest_pad(
        self, pad_locations: "list[location.Location]", curr_position: location.Location
    ) -> location.Location:
        """
        returns the location of the closest pad to the drone
        """

        if len(pad_locations) > 0:
            min_dist = float("inf")
            closest_pad = pad_locations[0]

            for pad_position in pad_locations:
                dist_to_pad = self.get_squared_distance(curr_position, pad_position)
                if dist_to_pad < min_dist:
                    closest_pad = pad_position
                    min_dist = dist_to_pad
            return closest_pad

        return curr_position
