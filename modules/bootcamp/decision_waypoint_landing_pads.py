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

        self.upper_flight_bound = 60
        self.lower_flight_bound = -60

        self.waypoint_found = False
        self.landing_location = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def location_in_bounds(self, loc: location.Location) -> bool:
        """
        Check to see if the waypoint is within flight bounds

        """
        return (
            loc.location_x <= self.upper_flight_bound
            and loc.location_x >= self.lower_flight_bound
            and loc.location_y <= self.upper_flight_bound
            and loc.location_y >= self.lower_flight_bound
        )

    def dist_sqr(self, drone: location.Location, obj: location.Location) -> float:
        """
        Find the square of the distance between drone and another object

        """
        return (drone.location_x - obj.location_x) ** 2 + (drone.location_y - obj.location_y) ** 2

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

        if not self.waypoint_found:

            if self.location_in_bounds(self.waypoint):

                x_dist_to_waypoint = self.waypoint.location_x - report.position.location_x
                y_dist_to_waypoint = self.waypoint.location_y - report.position.location_y

                # Distance between drone and waypoint squared (square root is costly)
                dist_to_waypoint_sqr = x_dist_to_waypoint**2 + y_dist_to_waypoint**2

                if report.status == drone_status.DroneStatus.HALTED:

                    # Case for when drone is halted but not at the waypoint (eg. start of simulation)
                    if dist_to_waypoint_sqr > self.acceptance_radius**2:
                        command = commands.Command.create_set_relative_destination_command(
                            x_dist_to_waypoint, y_dist_to_waypoint
                        )

                    # When drone reaches the waypoint
                    else:
                        self.waypoint_found = True

        else:
            # When closest landing pad hasn't been found yet
            if self.landing_location is None:
                shortest_distance = float("inf")

                # Finding the closest landing pad
                for landing_pad in landing_pad_locations:

                    cur_distance = self.dist_sqr(report.position, landing_pad)

                    if cur_distance < shortest_distance:
                        shortest_distance = cur_distance
                        self.landing_location = landing_pad

            # If landing pad is on the waypoint
            if (
                self.dist_sqr(report.position, self.landing_location) < self.acceptance_radius**2
                and report.status != drone_status.DroneStatus.HALTED
            ):

                return commands.Command.create_halt_command()

            # To get the drone to move to closest landing pad and land
            if self.location_in_bounds(self.landing_location):

                if report.status == drone_status.DroneStatus.HALTED:

                    if (
                        self.dist_sqr(report.position, self.landing_location)
                        > self.acceptance_radius**2
                    ):

                        x_dist_to_landing = (
                            self.landing_location.location_x - report.position.location_x
                        )
                        y_dist_to_landing = (
                            self.landing_location.location_y - report.position.location_y
                        )

                        command = commands.Command.create_set_relative_destination_command(
                            x_dist_to_landing, y_dist_to_landing
                        )

                    else:
                        command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
