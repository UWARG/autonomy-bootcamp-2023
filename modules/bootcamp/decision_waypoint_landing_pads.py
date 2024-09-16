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

        self.waypoint_found = False
        self.landing_pad_found = False

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
        if report.status == drone_status.DroneStatus.HALTED and not self.waypoint_found:
            if self.is_within_acceptance_radius(report.position, self.waypoint):
                self.waypoint_found = True
                print(f"reached waypoint at {self.waypoint.location_x}, {self.waypoint.location_y}")
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y
                )
                print(f"Moving to waypoint at {self.waypoint.location_x}, {self.waypoint.location_y}")

        elif report.status == drone_status.DroneStatus.HALTED and self.waypoint_found and not self.landing_pad_found:
            closest_pad = min(landing_pad_locations, key=lambda pad: self.distance(report.position, pad))
            if self.is_within_acceptance_radius(report.position, closest_pad):
                self.landing_pad_found = True
                print(f"reached landing pad at {closest_pad.location_x}, {closest_pad.location_y}")
            else:
                command = commands.Command.create_set_relative_destination_command(
                    closest_pad.location_x - report.position.location_x,
                    closest_pad.location_y - report.position.location_y
                )
                print(f"moving to landing pad at {closest_pad.location_x}, {closest_pad.location_y}")

        elif report.status == drone_status.DroneStatus.HALTED and self.landing_pad_found:
            command = commands.Command.create_land_command()
            print("Landing the drone.")

        return command

    def distance(self, l1: location.Location, l2: location.Location) -> float:
        return (l1.location_x - l2.location_x) ** 2 + (l1.location_y - l2.location_y) ** 2

    def is_within_acceptance_radius(self, pos1: location.Location, pos2: location.Location) -> bool:
        return self.distance(pos1, pos2) <= self.acceptance_radius ** 2
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        # return command
