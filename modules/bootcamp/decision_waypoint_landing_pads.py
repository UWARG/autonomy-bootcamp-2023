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

        self.waypoint_achieved = False
        self.final_destination = None

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

        if (
            report.status == drone_status.DroneStatus.HALTED
            and self.waypoint_achieved
            and (
                self.acceptance_radius**2
                >= self.find_squared_dist(self.final_destination, report.position)
            )
        ):
            # landing at closest landing pad
            command = command.create_land_command()
        elif report.status == drone_status.DroneStatus.HALTED and (
            self.acceptance_radius**2 >= self.find_squared_dist(self.waypoint, report.position)
        ):
            # find closest landing pad
            self.waypoint_achieved = True
            self.final_destination = self.find_closest_location(
                report.position, landing_pad_locations
            )

            if self.final_destination is not None:
                command = command.create_set_relative_destination_command(
                    self.final_destination.location_x - report.position.location_x,
                    self.final_destination.location_y - report.position.location_y,
                )
            else:
                # leave control of drone to higher-order function if no landing pad is available
                command = command.create_null_command()
        elif report.status == drone_status.DroneStatus.HALTED:
            command = command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x,
                self.waypoint.location_y - report.position.location_y,
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    # helper functions
    @staticmethod
    def find_squared_dist(loc1: location.Location, loc2: location.Location) -> int:
        """helper function that finds the squared distance between two Location instances"""
        return (loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2

    @staticmethod
    def find_closest_location(
        curr_loc: location.Location, location_list: "list[location.Location]"
    ) -> location.Location | None:
        """find the closest location in a list of locations"""
        min_dist, closest_location = float("inf"), None

        for loc in location_list:
            dist = DecisionWaypointLandingPads.find_squared_dist(curr_loc, loc)
            if dist < min_dist:
                closest_location = loc
                min_dist = dist

        return closest_location
