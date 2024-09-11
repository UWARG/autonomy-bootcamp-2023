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
        self.to_waypoint = True
        self.to_landing = False

        self.closest = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def closest_landing_pad(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Finds the closest landing pad given the current location of the drone.
        The assumption that the boundaries of the drone are from -60 to 60,
        it is possible to set a maximum squared distance of greater than 2 * 120**2,
        hence the initial distance is 1000000.
        """
        distance = 1000000
        idx = None
        for loc in landing_pad_locations:
            dist = (loc.location_x - report.position.location_x) ** 2 + (
                loc.location_y - report.position.location_y
            ) ** 2
            if dist < distance:
                idx = loc
                distance = dist
        return idx

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
        if self.to_waypoint:
            if (self.waypoint.location_x - report.position.location_x) ** 2 + (
                self.waypoint.location_y - report.position.location_y
            ) ** 2 <= self.acceptance_radius**2:
                self.to_waypoint = False
                self.to_landing = True
            elif not report.status == report.status.MOVING:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
        elif self.to_landing:
            if self.closest is None:
                self.closest = self.closest_landing_pad(report, landing_pad_locations)
                command = commands.Command.create_set_relative_destination_command(
                    self.closest.location_x - report.position.location_x,
                    self.closest.location_y - report.position.location_y,
                )
            elif (self.closest.location_x - report.position.location_x) ** 2 + (
                self.closest.location_y - report.position.location_y
            ) ** 2 <= self.acceptance_radius**2:
                self.to_landing = False
        else:
            if report.status == report.status.HALTED:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_halt_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
