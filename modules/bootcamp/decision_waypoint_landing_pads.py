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
        self.has_landed = False
        self.reached_waypoint = False
        self.closest_landing_pad = None

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
        if self.has_landed:
            return command

        if report.status.name == "LANDED":
            self.has_landed = True
            return command

        if not self.reached_waypoint:
            # Calculate distance to waypoint
            delta_x = self.waypoint.location_x - report.position.location_x
            delta_y = self.waypoint.location_y - report.position.location_y
            dist = (delta_x**2 + delta_y**2) ** 0.5

            if dist > self.acceptance_radius:
                if report.status.name == "HALTED":
                    command = commands.Command.create_set_relative_destination_command(delta_x, delta_y)
            else:
                self.reached_waypoint = True
                # Find closest landing pad
                min_dist = float("inf")
                for pad in landing_pad_locations:
                    pad_delta_x = pad.location_x - report.position.location_x
                    pad_delta_y = pad.location_y - report.position.location_y
                    pad_dist = (pad_delta_x**2 + pad_delta_y**2) ** 0.5
                    if pad_dist < min_dist:
                        min_dist = pad_dist
                        self.closest_landing_pad = pad
        else:
            # Move to closest landing pad
            delta_x = self.closest_landing_pad.location_x - report.position.location_x
            delta_y = self.closest_landing_pad.location_y - report.position.location_y
            dist = (delta_x**2 + delta_y**2) ** 0.5

            if dist > self.acceptance_radius:
                if report.status.name == "HALTED":
                    command = commands.Command.create_set_relative_destination_command(delta_x, delta_y)
            else:
                if report.status.name == "HALTED":
                    command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
