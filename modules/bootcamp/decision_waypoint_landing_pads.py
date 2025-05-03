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

        self.has_reached_waypoint = False
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

        position = report.position
        status = report.status
        
        dx = self.waypoint.location_x - position.location_x
        dy = self.waypoint.location_y - position.location_y
        distance_to_waypoint_squared = (dx**2) + (dy**2)
        
        if not self.has_reached_waypoint:
            if distance_to_waypoint_squared <= self.acceptance_radius ** 2:
                self.has_reached_waypoint = True
                min_distance_squared = float('inf')
                for pad in landing_pad_locations:
                    distance_squared = (pad.location_x - position.location_x) ** 2 + (pad.location_y - position.location_y) ** 2
                    if distance_squared < min_distance_squared:
                        min_distance_squared = distance_squared
                        self.closest_landing_pad = pad
            elif status == drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_set_relative_destination_command(dx, dy)
        elif self.closest_landing_pad:
            pad_dx = self.closest_landing_pad.location_x - position.location_x
            pad_dy = self.closest_landing_pad.location_y - position.location_y
            distance_to_pad_squared = (pad_dx**2) + (pad_dy**2)
            
            if distance_to_pad_squared <= self.acceptance_radius ** 2:
                if status == drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_land_command()
            elif status == drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_set_relative_destination_command(pad_dx, pad_dy)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
