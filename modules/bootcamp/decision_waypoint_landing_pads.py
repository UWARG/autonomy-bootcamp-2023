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

        self.waypoint_visited: bool = False
        self.target_landing_pad: location.Location = None

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
        if report.status == drone_status.DroneStatus.HALTED:
            if not self.visited_waypoint:
                target_x = self.waypoint.location_x
                target_y = self.waypoint.location_y
            else:
                if self.landing_pad_target is None:
                    min_distance_sq = float("inf")
                    nearest_pad: location.Location = None

                    for pad in landing_pad_locations:
                        distance_sq = (pad.location_x - report.position.location_x) ** 2 + (pad.location_y - report.position.location_y) ** 2
                        if distance_sq < min_distance_sq:
                            min_distance_sq = distance_sq
                            nearest_pad = pad
                    self.landing_pad_target = nearest_pad 
                if self.landing_pad_target:
                    target_x = self.landing_pad_target.location_x
                    target_y = self.landing_pad_target.location_y
                else:
                    return command

            distance_sq = (target_x - report.position.location_x) ** 2 + (target_y - report.position.location_y) ** 2

            if distance_sq < self.acceptance_radius**2:
                if not self.visited_waypoint:
                    self.visited_waypoint = True
                else:
                    command = commands.Command.create_land_command()
            else:
                offset_x = target_x - report.position.location_x
                offset_y = target_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(offset_x, offset_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command 
