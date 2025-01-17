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
    def _find_nearest_landing_pad(self, current_position: location.Location, landing_pad_locations: "list[location.Location]") -> location.Location:
        nearest_landing_pad = None
        min_distance = float('inf')

        for pad in landing_pad_locations:
            distance = pow(
                pow(pad.location_x - current_position.location_x, 2) +
                pow(pad.location_y - current_position.location_y, 2), 0.5
            )
            if distance < min_distance:
                min_distance = distance
                nearest_landing_pad = pad
        
        return nearest_landing_pad
    
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

        self.has_arrived_at_waypoint = False
        self.has_arrived_at_landing_pad = False

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

        current_position = report.position
        drone_status_value = report.status

        distance_to_waypoint = pow(
            pow(self.waypoint.location_x - current_position.location_x, 2) + 
            pow(self.waypoint.location_y - current_position.location_y, 2), 0.5
            )

        if not self.has_arrived_at_waypoint:
            if drone_status_value == drone_status.DroneStatus.HALTED and distance_to_waypoint > self.acceptance_radius:
                relative_x = self.waypoint.location_x - current_position.location_x
                relative_y = self.waypoint.location_y - current_position.location_y
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

            elif drone_status_value == drone_status.DroneStatus.HALTED and distance_to_waypoint <= self.acceptance_radius:
                self.has_arrived_at_waypoint = True
                nearest_landing_pad = self._find_nearest_landing_pad(current_position, landing_pad_locations)
                if nearest_landing_pad:
                    relative_x = nearest_landing_pad.location_x - current_position.location_x
                    relative_y = nearest_landing_pad.location_y - current_position.location_y
                    command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
                else:
                    command = commands.Command.create_land_command()

        if self.has_arrived_at_waypoint and not self.has_arrived_at_landing_pad:
            nearest_landing_pad = self._find_nearest_landing_pad(current_position, landing_pad_locations)
            if nearest_landing_pad:
                distance_to_landing_pad = pow(
                    pow(nearest_landing_pad.location_x - current_position.location_x, 2) + 
                    pow(nearest_landing_pad.location_y - current_position.location_y, 2), 0.5
                    )
                if distance_to_landing_pad <= self.acceptance_radius:
                    self.has_arrived_at_landing_pad = True
                    command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
