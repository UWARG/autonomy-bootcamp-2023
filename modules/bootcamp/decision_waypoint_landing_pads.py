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
        self.has_sent_landing_command = False
        self.landing_phase = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============``

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

        def calculate_norm_squared(p_1: location.Location, p_2: location.Location) -> float:
            # L2 norm squared (Euclidean distance squared)
            delta_dx = p_1.location_x - p_2.location_x
            delta_dy = p_1.location_y - p_2.location_y
            return delta_dx ** 2 + delta_dy ** 2

        position = report.position
        if report.status == drone_status.DroneStatus.HALTED:

            if not self.landing_phase:
                # Moving toward waypoint
                delta_dx = self.waypoint.location_x - position.location_x
                delta_dy = self.waypoint.location_y - position.location_y

                if abs(delta_dx) + abs(delta_dy) <= self.acceptance_radius:
                    # Reached waypoint, now we find the nearest landing pad
                    self.landing_phase = True
                else:
                    relative_x = (
                        min(max(position.location_x + delta_dx, -60), 60) - position.location_x
                    )
                    relative_y = (
                        min(max(position.location_y + delta_dy, -60), 60) - position.location_y
                    )
                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )
            else:
                # Moving toward the nearest landing pad
                closest_pad = None
                min_distance_sq = float("inf")

                for landing_pad in landing_pad_locations:
                    distance_sq = calculate_norm_squared(landing_pad, position)
                    if distance_sq < min_distance_sq:
                        min_distance_sq = distance_sq
                        closest_pad = landing_pad

                pad_dx = closest_pad.location_x - position.location_x
                pad_dy = closest_pad.location_y - position.location_y

                if not self.has_sent_landing_command:
                    if abs(pad_dx) + abs(pad_dy) <= self.acceptance_radius:

                        self.has_sent_landing_command = True
                        command = commands.Command.create_land_command()
                    else:
                        relative_x = (
                            min(max(position.location_x + pad_dx, -60), 60) - position.location_x
                        )
                        relative_y = (
                            min(max(position.location_y + pad_dy, -60), 60) - position.location_y
                        )
                        command = commands.Command.create_set_relative_destination_command(
                            relative_x, relative_y
                        )
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
