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
        self.closest_landing_x = float("inf")
        self.closest_landing_y = float("inf")

        """
        self.action_status[0] = travelling to waypoint
        self.action_status[1] = arrived at waypoint
        self.action_status[2] = travelling to landing pad
        self.action_status[3] = arrived at landing pad
        """
        self.action_status = [False, False, False, False]

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
            not self.action_status[0]
            or not self.action_status[1]
            and report.status.name == "HALTED"
        ):
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x,
                self.waypoint.location_y - report.position.location_y,
            )
            self.action_status[0] = True
        elif not self.action_status[1]:
            waypoint_dx = self.waypoint.location_x - report.position.location_x
            waypoint_dy = self.waypoint.location_y - report.position.location_y
            dist_from_accept = waypoint_dx * waypoint_dx + waypoint_dy * waypoint_dy
            if dist_from_accept <= self.acceptance_radius * self.acceptance_radius:
                self.action_status[1] = True
        elif (
            not self.action_status[2]
            or not self.action_status[3]
            and report.status.name == "HALTED"
        ):
            for loc in landing_pad_locations:
                current_from_landing = loc.location_x**2 + loc.location_y**2
                if current_from_landing < self.closest_landing_x**2 + self.closest_landing_y**2:
                    self.closest_landing_x = loc.location_x
                    self.closest_landing_y = loc.location_y
            command = commands.Command.create_set_relative_destination_command(
                self.closest_landing_x - report.position.location_x,
                self.closest_landing_y - report.position.location_y,
            )
            self.action_status[2] = True
        elif not self.action_status[3]:
            landing_dx = self.closest_landing_x - report.position.location_x
            landing_dy = self.closest_landing_y - report.position.location_y
            dist_from_landing = landing_dx * landing_dx + landing_dy * landing_dy
            if dist_from_landing <= self.acceptance_radius * self.acceptance_radius:
                self.action_status[3] = True
        elif report.status.name == "HALTED": #Once drone has visited all landmarks, send command to land
            command = commands.Command.create_land_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
