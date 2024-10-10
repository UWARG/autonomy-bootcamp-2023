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


def distance_between(
    location1: location.Location,
    location2: location.Location,
) -> int:
    """
    Finds the distance to a landing pad
    """
    distance_squared = (location2.location_x - location1.location_x) ** 2 + (
        location2.location_y - location1.location_y
    ) ** 2
    return distance_squared


def closest_landing_pad(
    report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
) -> location.Location:
    """
    Finds the closest landing pad
    """
    min_distance = float("inf")
    for landing_pad in landing_pad_locations:
        if distance_between(landing_pad, report.position) < min_distance:
            min_distance = distance_between(landing_pad, report.position)
            destination = landing_pad
    return destination


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
        self.arrived_waypoint = False
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
        if (
            report.status == report.status.HALTED
            and distance_between(
                report.position, closest_landing_pad(report, landing_pad_locations)
            )
            <= self.acceptance_radius**2
            and self.arrived_waypoint is True
        ):
            command = commands.Command.create_land_command()

        elif (
            report.status == report.status.HALTED
            and self.waypoint.location_x == report.position.location_x
            and self.arrived_waypoint is False
        ):
            self.arrived_waypoint = True
            command = commands.Command.create_set_relative_destination_command(
                closest_landing_pad(report, landing_pad_locations).location_x
                - report.position.location_x,
                closest_landing_pad(report, landing_pad_locations).location_y
                - report.position.location_y,
            )
        elif report.status == report.status.HALTED and self.arrived_waypoint is False:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
