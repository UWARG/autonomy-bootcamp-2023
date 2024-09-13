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

        self.landing_pad = None
        self.destination = self.waypoint
        self.arrived_at_waypoint = False

        # ============

    def find_closest_landing_pad(self, landing_pad_list: location.Location, current_x, current_y):
        """
        When given a list of landing pads, it will find the one closest to your current location
        """
        closest_landing_pad = None
        dist_from_drone = None

        for landing_pad in landing_pad_list:
            dist = (landing_pad.location_x - current_x) ** 2 + (
                landing_pad.location_y - current_y
            ) ** 2

            if dist_from_drone is None:
                dist_from_drone = dist
                closest_landing_pad = landing_pad

            else:
                if dist_from_drone > dist:
                    dist = dist_from_drone
                    closest_landing_pad = landing_pad

        return closest_landing_pad

    def relative_distance_to_location(
        self, current_x, current_y, desired_location: location.Location
    ):
        """
        Finds how far you are from the location you want to get to based off your current location
        """
        return (desired_location.location_x - current_x), (desired_location.location_y - current_y)

    def at_location(self, current_x, current_y, desired_location: location.Location):
        """
        Returns if you are at the location you wanted or not
        """
        dist_to_location = sum(
            dist**2
            for dist in self.relative_distance_to_location(current_x, current_y, desired_location)
        )
        if dist_to_location <= self.acceptance_radius**2:
            return True
        return False

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

        current_x, current_y = report.position.location_x, report.position.location_y

        if report.status == drone_status.DroneStatus.HALTED and not self.at_location(
            current_x, current_y, self.destination
        ):

            relative_x_dist_to_destination, relative_y_dist_to_destination = (
                self.relative_distance_to_location(current_x, current_y, self.destination)
            )
            command = commands.Command.create_set_relative_destination_command(
                relative_x_dist_to_destination, relative_y_dist_to_destination
            )

        elif report.status == drone_status.DroneStatus.HALTED and self.at_location(
            current_x, current_y, self.destination
        ):

            if self.arrived_at_waypoint:
                command = commands.Command.create_land_command()

            else:
                self.destination = self.find_closest_landing_pad(
                    landing_pad_locations, current_x, current_y
                )

        else:
            print("Something goofed RIP")
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
