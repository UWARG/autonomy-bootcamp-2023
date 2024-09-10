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
        self.landing_pad = None
        self.has_reached_waypoint = False
        self.has_sent_landing_command = False

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
            if not self.has_reached_waypoint and report.position != self.waypoint:
                print(f"Halted at: {report.position}, moving to waypoint")
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x, self.waypoint.location_y
                )
            elif not self.has_reached_waypoint and report.position == self.waypoint:
                self.has_reached_waypoint = True
                print(f"Halted at: {report.position}, reached waypoint")
                self.waypoint = self.determine_closest_landing_pad(
                    self.waypoint, landing_pad_locations
                )
                if (
                    self.calculate_distance(report.position, self.landing_pad)
                    < self.acceptance_radius**2
                ):
                    print(f"Already at the closest landing pad: {report.position}, landing")
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.landing_pad.location_x, self.landing_pad.location_y
                    )
            elif (
                self.has_reached_waypoint
                and self.calculate_distance(report.position, self.landing_pad)
                < self.acceptance_radius**2
                and not self.has_sent_landing_command
            ):
                print(f"Halted at: {report.position}, landing")
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True
            elif (
                self.has_reached_waypoint
                and self.calculate_distance(report.position, self.landing_pad)
                >= self.acceptance_radius**2
            ):
                print(f"Halted at: {report.position}, moving to landing pad")
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x, self.waypoint.location_y
                )
        else:
            # If the drone is moving, send a null command to continue the simulation
            command = commands.Command.create_null_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def determine_closest_landing_pad(
        self, waypoint_location: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        """
        Returns relative location to nearest landing pad
        """
        max_distance = float("inf")
        for landing_pad_location in landing_pad_locations:
            distance = self.calculate_distance(waypoint_location, landing_pad_location)
            if distance < max_distance:
                max_distance = distance
                self.landing_pad = landing_pad_location

        return location.Location(
            self.landing_pad.location_x - waypoint_location.location_x,
            self.landing_pad.location_y - waypoint_location.location_y,
        )

    def calculate_distance(self, loc1: location.Location, loc2: location.Location) -> float:
        """
        Calculate the L-2 norm (Euclidean distance) between two locations.
        """
        return (loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2
