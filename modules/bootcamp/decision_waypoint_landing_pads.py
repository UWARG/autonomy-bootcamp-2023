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

        self.waypoint_found = False  # Tracks if the waypoint has been reached
        self.landing_pad_found = False  # Tracks if the landing pad has been reached
        self.closest_pad = None

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

        if report.status != drone_status.DroneStatus.HALTED:
            return command

        # If the waypoint has not yet been reached
        if not self.waypoint_found:
            # Calculate the difference between the current position and the waypoint
            delta_x = abs(report.position.location_x - self.waypoint.location_x)
            delta_y = abs(report.position.location_y - self.waypoint.location_y)

            # Check if the drone is within the acceptance radius for both x and y coordinates
            if delta_x <= self.acceptance_radius and delta_y <= self.acceptance_radius:
                self.waypoint_found = True
                print(f"Reached waypoint at {self.waypoint.location_x}, {self.waypoint.location_y}")
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
                print(
                    f"Moving to waypoint at {self.waypoint.location_x}, {self.waypoint.location_y}"
                )
                return command

        # If the waypoint is reached but landing pad not found yet
        if self.waypoint_found and not self.landing_pad_found:
            # Find the closest landing pad only once
            if self.closest_pad is None:
                self.closest_pad = min(
                    landing_pad_locations,
                    key=lambda pad: (pad.location_x - report.position.location_x) ** 2
                    + (pad.location_y - report.position.location_y) ** 2,
                )
                print(
                    f"Closest landing pad determined at {self.closest_pad.location_x}, {self.closest_pad.location_y}"
                )

            # Calculate the difference between the current position and the closest landing pad
            delta_x = abs(report.position.location_x - self.closest_pad.location_x)
            delta_y = abs(report.position.location_y - self.closest_pad.location_y)

            # Move towards the closest landing pad
            if delta_x <= self.acceptance_radius and delta_y <= self.acceptance_radius:
                self.landing_pad_found = True
                print(
                    f"Reached landing pad at {self.closest_pad.location_x}, {self.closest_pad.location_y}"
                )
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.closest_pad.location_x - report.position.location_x,
                    self.closest_pad.location_y - report.position.location_y,
                )
                print(
                    f"Moving to landing pad at {self.closest_pad.location_x}, {self.closest_pad.location_y}"
                )
                return command

        # If the drone has reached both the waypoint and the landing pad, land the drone
        if self.waypoint_found and self.landing_pad_found:
            command = commands.Command.create_land_command()
            print("Landing the drone.")
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
