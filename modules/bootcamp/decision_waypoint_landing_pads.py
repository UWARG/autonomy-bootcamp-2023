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
        self.nearest_landingpad = None

        self.acceptance_radius_squared = acceptance_radius**2

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
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
        distance_to_waypoint = (self.waypoint.location_x - report.position.location_x) ** 2 + (
            self.waypoint.location_y - report.position.location_y
        ) ** 2
        distance_to_landingpad = (
            (self.nearest_landingpad.location_x - report.position.location_x) ** 2
            + (self.nearest_landingpad.location_y - report.position.location_y) ** 2
            if self.nearest_landingpad is not None
            else None
        )
        if (
            report.status == drone_status.DroneStatus.HALTED
            and not report.status == drone_status.DroneStatus.LANDED
        ):

            if (
                distance_to_landingpad is not None
                and distance_to_landingpad < self.acceptance_radius_squared
            ):
                command = commands.Command.create_land_command()
            elif distance_to_waypoint < self.acceptance_radius_squared:
                shortest_distance = float("inf")

                for landing_pad in landing_pad_locations:
                    distance = landing_pad.location_x**2 + landing_pad.location_y**2

                    if shortest_distance > distance:
                        shortest_distance = distance
                        self.nearest_landingpad = landing_pad

                if self.nearest_landingpad is not None:
                    command = commands.Command.create_set_relative_destination_command(
                        self.nearest_landingpad.location_x - report.position.location_x,
                        self.nearest_landingpad.location_y - report.position.location_y,
                    )
                else:
                    command = commands.Command.create_null_command()
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
        elif report.status == drone_status.DroneStatus.MOVING:
            if distance_to_waypoint < self.acceptance_radius_squared:
                command = commands.Command.create_halt_command()
            if (
                distance_to_landingpad is not None
                and distance_to_landingpad < self.acceptance_radius_squared
            ):
                commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
