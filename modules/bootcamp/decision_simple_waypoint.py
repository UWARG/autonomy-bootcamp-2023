"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
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

        self.waypoint_reached = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

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
        # Calculate the squared distance for efficiency (avoiding square root calculation)
        delta_x = self.waypoint.location_x - report.position.location_x
        delta_y = self.waypoint.location_y - report.position.location_y
        distance_squared = delta_x ** 2 + delta_y ** 2
        acceptance_radius_squared = self.acceptance_radius ** 2

        # Evaluate based on the drone's current status
        if report.status == drone_status.DroneStatus.HALTED:
            if distance_squared <= acceptance_radius_squared:
                self.has_reached_waypoint = True
                command = commands.Command.create_land_command()
                print("Drone has reached the destination and is landing.")
            else:
                command = commands.Command.create_set_relative_destination_command(
                    delta_x, delta_y
                )
                print("Drone is on the move to the waypoint.")

        elif report.status == drone_status.DroneStatus.MOVING:
            if distance_squared <= acceptance_radius_squared:
                if not self.has_reached_waypoint:
                    self.has_reached_waypoint = True
                    print("Drone has reached the waypoint and is preparing to land.")
                command = commands.Command.create_halt_command()
            else:
                print("Drone is in transit to the waypoint.")
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
