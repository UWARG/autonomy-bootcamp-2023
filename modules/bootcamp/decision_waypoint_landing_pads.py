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

        self.heading_to_landing_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def reached_waypoint(self, pos_x: float, pos_y: float) -> bool:
        """
        Check if the drone has reached the waypoint.
        """
        return (self.waypoint.location_x - pos_x) ** 2 + (
            self.waypoint.location_y - pos_y
        ) ** 2 <= self.acceptance_radius**2

    def reached_landing_pad(
        self, pos_x: float, pos_y: float, landing_pad: location.Location
    ) -> bool:
        """
        Calculate the distance between the drone and a landing pad.
        """
        return (landing_pad.location_x - pos_x) ** 2 + (
            landing_pad.location_y - pos_y
        ) ** 2 <= self.acceptance_radius**2

    def pick_nearest_landing_pad(
        self, pos_x: float, pos_y: float, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        """
        Pick the nearest landing pad.
        """
        nearest_landing_pad = None
        distance_from_nearest_landing_pad_squared = 100000000

        for i in landing_pad_locations:
            if (i.location_x - pos_x) ** 2 + (
                i.location_y - pos_y
            ) ** 2 < distance_from_nearest_landing_pad_squared:
                nearest_landing_pad = i
                distance_from_nearest_landing_pad_squared = (i.location_x - pos_x) ** 2 + (
                    i.location_y - pos_y
                ) ** 2

        return nearest_landing_pad

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

        if not self.heading_to_landing_pad:
            if report.status == drone_status.DroneStatus.HALTED and self.reached_waypoint(
                report.position.location_x, report.position.location_y
            ):
                # Head to landing pad
                self.heading_to_landing_pad = True
            elif report.status == drone_status.DroneStatus.HALTED and not self.reached_waypoint(
                report.position.location_x, report.position.location_y
            ):
                # Move to waypoint
                dx = self.waypoint.location_x - report.position.location_x
                dy = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(dx, dy)
            else:
                # Let the simulation keep running if the drone is moving
                command = commands.Command.create_null_command()
        else:
            if report.status == drone_status.DroneStatus.HALTED and self.reached_landing_pad(
                report.position.location_x,
                report.position.location_y,
                self.pick_nearest_landing_pad(
                    report.position.location_x, report.position.location_y, landing_pad_locations
                ),
            ):
                # Head to landing pad
                command = commands.Command.create_land_command()
            elif report.status == drone_status.DroneStatus.HALTED and not self.reached_landing_pad(
                report.position.location_x,
                report.position.location_y,
                self.pick_nearest_landing_pad(
                    report.position.location_x, report.position.location_y, landing_pad_locations
                ),
            ):
                # Move to waypoint
                dx = (
                    self.pick_nearest_landing_pad(
                        report.position.location_x,
                        report.position.location_y,
                        landing_pad_locations,
                    ).location_x
                    - report.position.location_x
                )
                dy = (
                    self.pick_nearest_landing_pad(
                        report.position.location_x,
                        report.position.location_y,
                        landing_pad_locations,
                    ).location_y
                    - report.position.location_y
                )
                command = commands.Command.create_set_relative_destination_command(dx, dy)
            else:
                # Let the simulation keep running if the drone is moving
                command = commands.Command.create_null_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
