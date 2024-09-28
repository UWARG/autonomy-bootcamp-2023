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
        self.has_set_landing_command = False
        self.waypoint_reached = False
        self.closest_landing_pad_loc = None

    def get_distance_squared(self, loc1: location.Location, loc2: location.Location) -> float:
        """
        Returns the distance squared between two locations.

        Args:
            loc1 (location.Location): Location 1
            loc2 (location.Location): Location 2

        Returns:
            float: Distance squared between the two given locations
        """

        return (loc2.location_x - loc1.location_x) + (loc2.location_y - loc1.location_y)

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
            # Drone is halted
            if self.has_set_landing_command:
                # Drone is not halted and has reached its destination
                command = commands.Command.create_land_command()
            elif self.waypoint_reached and not self.closest_landing_pad_loc:
                shortest_dist = float("inf")
                for loc in landing_pad_locations:
                    dist = self.get_distance_squared(report.position, loc)
                    if dist < shortest_dist:
                        shortest_dist = dist
                        self.closest_landing_pad_loc = loc
            elif self.waypoint_reached and self.closest_landing_pad_loc:
                command = commands.Command.create_set_relative_destination_command(
                    self.closest_landing_pad_loc.location_x - report.position.location_x,
                    self.closest_landing_pad_loc.location_y - report.position.location_y,
                )
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
        elif report.status == drone_status.DroneStatus.MOVING:
            if (
                self.waypoint_reached
                and self.closest_landing_pad_loc
                and abs(report.position.location_x - self.closest_landing_pad_loc.location_x)
                <= self.acceptance_radius
                and abs(report.position.location_y - self.closest_landing_pad_loc.location_y)
                <= self.acceptance_radius
            ):
                command = commands.Command.create_halt_command()
                self.has_set_landing_command = True
            elif (
                abs(report.position.location_x - self.waypoint.location_x) <= self.acceptance_radius
                and abs(report.position.location_y - self.waypoint.location_y)
                <= self.acceptance_radius
            ):
                command = commands.Command.create_halt_command()
                self.waypoint_reached = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
