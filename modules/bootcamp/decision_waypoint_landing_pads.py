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


def calculate_distance(position: location.Location, landing_pad: location.Location) -> float:
    """
    Calculate the Euclidean distance between a given position and a landing pad.

    Args:
        position (object): An object with attributes `location_x` and `location_y` representing the coordinates of the position.
        landing_pad (object): An object with attributes `location_x` and `location_y` representing the coordinates of the landing pad.

    Returns:
        float: The Euclidean distance between the position and the landing pad.
    """
    return (
        (landing_pad.location_x - position.location_x) ** 2
        + (landing_pad.location_y - position.location_y) ** 2
    ) ** 0.5


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

        # a boolean to see if the drone has reached the waypoint
        self.reached = False

        self.nearest_landing_pad = None

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

        status = report.status
        position = report.position

        if not self.reached:
            distance_from_waypoint = (
                (self.waypoint.location_x - position.location_x) ** 2
                + (self.waypoint.location_y - position.location_y) ** 2
            ) ** 0.5

            # if the drone is in the acceptance radius, we have reached
            if distance_from_waypoint < self.acceptance_radius:
                self.reached = True
                self.nearest_landing_pad = min(
                    landing_pad_locations,
                    key=lambda landing_pad: calculate_distance(position, landing_pad),
                )
                relative_destination = location.Location(
                    self.nearest_landing_pad.location_x - position.location_x,
                    self.nearest_landing_pad.location_y - position.location_y,
                )
                return commands.Command.create_set_relative_destination_command(
                    relative_destination.location_x, relative_destination.location_y
                )
                # return commands.Command.create_halt_command()
            # otherwise, the drone has not reached in the acceptance radius
            # If the drone is not at the waypoint yet
            if status == drone_status.DroneStatus.HALTED:
                relative_destination = location.Location(
                    self.waypoint.location_x - position.location_x,
                    self.waypoint.location_y - position.location_y,
                )
                return commands.Command.create_set_relative_destination_command(
                    relative_destination.location_x, relative_destination.location_y
                )
            return command
        distance_to_pad = calculate_distance(position, self.nearest_landing_pad)
        # if we are within the acceptance radius of the landing pad, we land
        if distance_to_pad < self.acceptance_radius:
            if status == drone_status.DroneStatus.HALTED:
                return commands.Command.create_land_command()
            return commands.Command.create_halt_command()
        # if we are not within the acceptance radius of the landing pad, we head towards it
        if status == drone_status.DroneStatus.HALTED:
            relative_destination = location.Location(
                self.nearest_landing_pad.location_x - position.location_x,
                self.nearest_landing_pad.location_y - position.location_y,
            )
            return commands.Command.create_set_relative_destination_command(
                relative_destination.location_x, relative_destination.location_y
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
