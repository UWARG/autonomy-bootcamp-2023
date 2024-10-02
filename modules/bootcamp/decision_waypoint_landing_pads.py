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


def distance_to_landing_pad(
    landing_pad_x: location.Location,
    landing_pad_y: location.Location,
    position_x: location.Location,
    position_y: location.Location,
) -> int:
    """
    Finds the distance to a landing pad
    """
    distance = ((landing_pad_x - position_x) ** 2 + (landing_pad_y - position_y) ** 2) ** (1 / 2)
    return distance


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
            and report.position.location_x == 0
            and report.position.location_y == 0
        ):
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
        elif (
            report.status == report.status.HALTED
            and report.position.location_x == self.waypoint.location_x
            and report.position.location_y == self.waypoint.location_y
        ):
            command = commands.Command.create_halt_command()
            min_distance = 100000000000
            for landing_pad in landing_pad_locations:
                if (
                    distance_to_landing_pad(
                        landing_pad.location_x,
                        landing_pad.location_y,
                        report.position.location_x,
                        report.position.location_y,
                    )
                    < min_distance
                ):
                    min_distance = distance_to_landing_pad(
                        landing_pad.location_x,
                        landing_pad.location_y,
                        report.position.location_x,
                        report.position.location_y,
                    )
                    destination = landing_pad
            command = commands.Command.create_set_relative_destination_command(
                destination.location_x - report.position.location_x,
                destination.location_y - report.position.location_y,
            )
        elif report.status == report.status.HALTED and report.position == destination:
            command = commands.Command.create_land_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
