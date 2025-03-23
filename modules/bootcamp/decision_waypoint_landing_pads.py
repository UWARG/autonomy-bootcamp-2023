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
        self.waypoint_x = waypoint.location_x
        self.waypoint_y = waypoint.location_y
        self.reached_waypoint = False
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
        drone_x_pos = report.position.location_x
        drone_y_pos = report.position.location_y
        x_difference = self.waypoint_x - drone_x_pos
        y_difference = self.waypoint_y - drone_y_pos
        distance_squared = x_difference ** 2 + y_difference ** 2
        if not self.reached_waypoint:
            if distance_squared <= self.acceptance_radius ** 2:
                self.reached_waypoint = True
                nearest_pad_index = 0
                nearest_distance = (landing_pad_locations[0].location_x - drone_x_pos) ** 2 + (landing_pad_locations[0].location_y - drone_y_pos) ** 2

                for i in range(1, len(landing_pad_locations)):
                    current_distance = (landing_pad_locations[i].location_x - drone_x_pos) ** 2 + (landing_pad_locations[i].location_y - drone_y_pos) ** 2
                    if current_distance < nearest_distance:
                        nearest_pad_index = i
                        nearest_distance = current_distance
                self.nearest_pad_index = nearest_pad_index
            else:
                command = commands.Command.create_set_relative_destination_command(
                    x_difference, y_difference
                )
        if self.reached_waypoint:
            nearest_pad = landing_pad_locations[self.nearest_pad_index]
            pad_x_diff = nearest_pad.location_x - drone_x_pos
            pad_y_diff = nearest_pad.location_y - drone_y_pos
            pad_distance_squared = pad_x_diff ** 2 + pad_y_diff ** 2

            if pad_distance_squared <= self.acceptance_radius ** 2:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(
                    pad_x_diff, pad_y_diff
                )
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
