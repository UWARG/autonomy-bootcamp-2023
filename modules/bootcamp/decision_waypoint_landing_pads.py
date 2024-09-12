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

        # Add your own
        self.route_status = "waypoint"

        self.closest = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def closest_landing_pad(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location] | None",
    ) -> commands.Command:
        """
        Finds the closest landing pad given the current location of the drone.
        """
        min_distance = float("inf")
        closest_landing_pad_location = None
        for landing_pad_location in landing_pad_locations:
            distance_to_landing_pad = (
                landing_pad_location.location_x - report.position.location_x
            ) ** 2 + (landing_pad_location.location_y - report.position.location_y) ** 2
            if distance_to_landing_pad < min_distance:
                closest_landing_pad_location = landing_pad_location
                min_distance = distance_to_landing_pad
        return closest_landing_pad_location

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

        if self.route_status == "landing":
            if report.status == report.status.HALTED:
                command = commands.Command.create_land_command()
                self.route_status = "landed"
            else:
                command = commands.Command.create_halt_command()
        elif self.route_status == "landed":
            command = commands.Command.create_null_command()
        else:
            if self.route_status == "waypoint":
                destination = self.waypoint
            elif self.route_status == "pad":
                if self.closest is None:
                    self.closest = self.closest_landing_pad(report, landing_pad_locations)
                destination = self.closest
            if (destination.location_x - report.position.location_x) ** 2 + (
                destination.location_y - report.position.location_y
            ) ** 2 <= self.acceptance_radius**2:
                if self.route_status == "waypoint":
                    self.route_status = "pad"
                elif self.route_status == "pad":
                    self.route_status = "landing"
            elif report.status != report.status.MOVING:
                command = commands.Command.create_set_relative_destination_command(
                    destination.location_x - report.position.location_x,
                    destination.location_y - report.position.location_y,
                )
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
