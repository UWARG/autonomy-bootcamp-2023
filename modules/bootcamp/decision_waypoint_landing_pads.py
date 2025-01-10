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

        self.reached_waypoint = False
        self.closest_pad = None

    def calculate_squared_distance(
            self, loc1: location.Location, loc2: location.Location
        ) -> float:
            dx = loc1.location_x - loc2.location_x 
            dy = loc1.location_y - loc2.location_y
            return dx * dx + dy * dy
    
    def set_closest_pad(
        self, position: location.Location, landing_pads: "list[location.Location]"
    ) -> None:
        nearest_distance = float("inf")
        for landing_pad in landing_pads:
            landing_pad_distance = self.calculate_squared_distance(position, landing_pad)
            if landing_pad_distance < nearest_distance:
                nearest_distance = landing_pad_distance
                self.closest_pad = landing_pad

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

        waypoint_position = self.waypoint
        current_position = report.position

        if not self.reached_waypoint:
            if (
                self.calculate_squared_distance(current_position, waypoint_position) < self.acceptance_radius**2
            ):
                self.set_closest_pad(current_position, landing_pad_locations)
                self.reached_waypoint = True
            else:
                command = commands.Command.create_set_relative_destination_command(
                    waypoint_position.location_x - current_position.location_x,
                    waypoint_position.location_y - current_position.location_y,
                )

        else:
            if (
                self.calculate_squared_distance(current_position, self.closest_pad) < self.acceptance_radius**2
            ):
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.closest_pad.location_x - current_position.location_x,
                    self.closest_pad.location_y - current_position.location_y,
                )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
