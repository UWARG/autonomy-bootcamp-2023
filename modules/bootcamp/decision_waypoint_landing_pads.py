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

    def _find_nearest_landing_pad(
        self, current_position: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        nearest_landing_pad = None
        min_distance = float("inf")

        for pad in landing_pad_locations:
            distance_x = pad.location_x - current_position.location_x
            distance_y = pad.location_y - current_position.location_y

            distance = distance_x**2 + distance_y**2

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
        self.nearest_landing_pad = None

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

        relative_x = self.waypoint.location_x - current_position.location_x
        relative_y = self.waypoint.location_y - current_position.location_y
        distance_to_waypoint = relative_x**2 + relative_y**2

        if not self.has_arrived_at_waypoint:
            if distance_to_waypoint > self.acceptance_radius**2:
                command = commands.Command.create_set_relative_destination_command(
                    relative_x, relative_y
                )
            else:
                self.has_arrived_at_waypoint = True
                self.nearest_landing_pad = self._find_nearest_landing_pad(
                    current_position, landing_pad_locations
                )

        if self.has_arrived_at_waypoint and not self.has_arrived_at_landing_pad:
            if self.nearest_landing_pad:
                landing_x = self.nearest_landing_pad.location_x - current_position.location_x
                landing_y = self.nearest_landing_pad.location_y - current_position.location_y
                distance_to_landing_pad = landing_x**2 + landing_y**2

                if distance_to_landing_pad > self.acceptance_radius**2:
                    command = commands.Command.create_set_relative_destination_command(
                        landing_x, landing_y
                    )
                else:
                    self.has_arrived_at_landing_pad = True
                    command = commands.Command.create_land_command()
            else:
                self.has_arrived_at_landing_pad = True
                command = commands.Command.create_land_command()

        if self.has_arrived_at_landing_pad:
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
