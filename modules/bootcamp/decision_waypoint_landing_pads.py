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

        self.has_gone_to_waypoint = False

        self.has_sent_landing_command = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def get_squared_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """
        Calculate the distance between two points and return its square
        """
        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

    def get_closest_landing_pad(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> int:
        """
        Find the closest landing pad to the drone.
        """
        closest_landing_pad = 0
        for i in range(1, len(landing_pad_locations)):
            if self.get_squared_distance(
                report.position.location_x,
                report.position.location_y,
                landing_pad_locations[i].location_x,
                landing_pad_locations[i].location_y,
            ) < self.get_squared_distance(
                report.position.location_x,
                report.position.location_y,
                landing_pad_locations[closest_landing_pad].location_x,
                landing_pad_locations[closest_landing_pad].location_y,
            ):
                closest_landing_pad = i
        return closest_landing_pad

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

        # If the drone is at its desired location, then you must have reached the waypoint
        if (
            self.get_squared_distance(
                report.position.location_x,
                report.position.location_y,
                self.waypoint.location_x,
                self.waypoint.location_y,
            )
            < self.acceptance_radius * self.acceptance_radius
        ):
            self.has_gone_to_waypoint = True

        # If the drone has gone to the waypoint, calculate the direction to the closest landing pad
        if self.has_gone_to_waypoint:

            closest_landing_pad = self.get_closest_landing_pad(report, landing_pad_locations)

            direction_coordinate_x = (
                landing_pad_locations[closest_landing_pad].location_x - report.position.location_x
            )
            direction_coordinate_y = (
                landing_pad_locations[closest_landing_pad].location_y - report.position.location_y
            )

        else:
            direction_coordinate_x = self.waypoint.location_x - report.position.location_x
            direction_coordinate_y = self.waypoint.location_y - report.position.location_y

        # If the drone is halted and not at the waypoint, send a command to move to the waypoint
        # Also handles if the drone is not on the target after landing
        if (
            report.status in (drone_status.DroneStatus.HALTED, drone_status.DroneStatus.LANDED)
        ) and (
            direction_coordinate_x * direction_coordinate_x
            + direction_coordinate_y * direction_coordinate_y
        ) >= self.acceptance_radius * self.acceptance_radius:
            command = commands.Command.create_set_relative_destination_command(
                direction_coordinate_x, direction_coordinate_y
            )
        # If the drone is halted, at the waypoint, not already landed, send a command to land
        elif (
            report.status == drone_status.DroneStatus.HALTED
            and self.has_gone_to_waypoint
            and not self.has_sent_landing_command
        ):
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
