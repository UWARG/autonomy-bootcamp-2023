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
        self.closest_landing_pad = None

    def get_distance_squared(self, loc1: location.Location, loc2: location.Location) -> float:
        """Returns the distance squared between two locations"""
        return abs((loc2.location_x - loc1.location_x) + (loc2.location_y - loc1.location_y))

    def get_closest_landing_pad(
        self, pos: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> location.Location | None:
        shortest_dist = float("inf")
        closest_landing_pad = None
        for loc in landing_pad_locations:
            dist = self.get_distance_squared(pos, loc)
            if dist < shortest_dist:
                shortest_dist = dist
                closest_landing_pad = loc
        return closest_landing_pad

    def within_range(
        self, loc: location.Location, target: location.Location, radius: float
    ) -> bool:
        return (target.location_x - loc.location_x) ** 2 + (
            target.location_y - loc.location_y
        ) ** 2 < self.acceptance_radius**2

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
        if report.status == drone_status.DroneStatus.HALTED:
            if self.within_range(report.position, self.waypoint, self.acceptance_radius):
                # Drone has reached its waypoint, calculate nearest landing pad
                self.closest_landing_pad = self.get_closest_landing_pad(
                    report.position, landing_pad_locations
                )
                if self.closest_landing_pad:
                    command = commands.Command.create_set_relative_destination_command(
                        self.closest_landing_pad.location_x - report.position.location_x,
                        self.closest_landing_pad.location_y - report.position.location_y,
                    )
            elif self.closest_landing_pad and self.within_range(
                report.position, self.closest_landing_pad, self.acceptance_radius
            ):
                # Drone has reached its nearest landing pad
                command = commands.Command.create_land_command()
            else:
                # Create move command towards waypoint
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
