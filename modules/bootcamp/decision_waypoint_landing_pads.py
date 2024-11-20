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

    @staticmethod
    def l2_norm(x1: float, y1: float, x2: float, y2: float) -> float:
        """
        Calculate the L2 norm between two points.
        """
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def closest_pad(
        self, landing_pad_locations: "list[location.Location]", position: location.Location
    ) -> "tuple[float, float]":
        """
        Find the closest landing pad.
        """
        min_distance = float("inf")
        closest_pad_coords = (None, None)

        for landing_pad in landing_pad_locations:
            distance = self.l2_norm(
                position.location_x,
                position.location_y,
                landing_pad.location_x,
                landing_pad.location_y,
            )
            if distance < min_distance:
                min_distance = distance
                closest_pad_coords = (landing_pad.location_x, landing_pad.location_y)

        return closest_pad_coords

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

        self.waypoint_reached = False
        self.closest_pad_reached = False
        self.closest_pad_x = None
        self.closest_pad_y = None

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
            if not self.waypoint_reached:
                # Check if the drone is at the waypoint
                if (
                    (self.waypoint.location_x - report.position.location_x) ** 2
                    + (self.waypoint.location_y - report.position.location_y) ** 2
                ) ** 0.5 <= self.acceptance_radius:
                    self.waypoint_reached = True
                else:
                    # Move toward the waypoint
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y,
                    )
                    print("Drone is moving to the waypoint.")

            else:
                if self.closest_pad_x is None and self.closest_pad_y is None:
                    # Calculate closest pad relative to the drone's current position
                    self.closest_pad_x, self.closest_pad_y = self.closest_pad(
                        landing_pad_locations, self.waypoint
                    )

                if (
                    (self.closest_pad_x - report.position.location_x) ** 2
                    + (self.closest_pad_y - report.position.location_y) ** 2
                ) ** 0.5 <= self.acceptance_radius:
                    self.closest_pad_reached = True
                    command = commands.Command.create_land_command()
                else:
                    # Move toward the closest landing pad
                    command = commands.Command.create_set_relative_destination_command(
                        self.closest_pad_x - report.position.location_x,
                        self.closest_pad_y - report.position.location_y,
                    )
                    print("Drone is moving to the closest landing pad.")

        elif report.status == drone_status.DroneStatus.MOVING:
            if not self.waypoint_reached:
                # Check if the drone has reached the waypoint
                if (
                    (self.waypoint.location_x - report.position.location_x) ** 2
                    + (self.waypoint.location_y - report.position.location_y) ** 2
                ) ** 0.5 <= self.acceptance_radius:
                    self.waypoint_reached = True
                    command = commands.Command.create_halt_command()
                else:
                    print("Drone is moving towards the waypoint.")
            elif not self.closest_pad_reached:
                # Check if the drone has reached the closest landing pad
                if (
                    (self.closest_pad_x - report.position.location_x) ** 2
                    + (self.closest_pad_y - report.position.location_y) ** 2
                ) ** 0.5 <= self.acceptance_radius:
                    self.closest_pad_reached = True
                    command = commands.Command.create_halt_command()
                else:
                    print("Drone is moving towards the closest landing pad.")

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
