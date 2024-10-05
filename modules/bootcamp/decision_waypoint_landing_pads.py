"""
BOOTCAMPERS TO COMPLETE.

Travel to the designated waypoint and then land at a nearby landing pad.
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
    Travel to the designated waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        self.halt_at_initialization = True
        self.has_reached_waypoint = False
        self.closest_landing_pad = None

    def squared_distance(self, point1: location.Location, point2: location.Location) -> float:
        """
        Calculate the squared distance between two locations.
        """
        diff_distance_x = point1.location_x - point2.location_x
        diff_distance_y = point1.location_y - point2.location_y
        distance_net_squared = (diff_distance_x**2) + (diff_distance_y**2)
        return distance_net_squared

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        command = commands.Command.create_null_command()

        # get  current position
        current_position = report.position
        distance_net_squared = self.squared_distance(self.waypoint, current_position)

        if report.status == drone_status.DroneStatus.HALTED:
            # check if at the waypoint
            if not self.has_reached_waypoint and distance_net_squared <= self.acceptance_radius**2:
                command = commands.Command.create_land_command()
                print("Drone is landing at the waypoint!")
                self.has_reached_waypoint = True

            elif not self.has_reached_waypoint:
                diff_distance_x = self.waypoint.location_x - current_position.location_x
                diff_distance_y = self.waypoint.location_y - current_position.location_y
                command = commands.Command.create_set_relative_destination_command(
                    diff_distance_x, diff_distance_y
                )
                print("Going to waypoint!")
                self.has_reached_waypoint = False

            # find the closest landing pad
            if self.has_reached_waypoint and not self.closest_landing_pad:
                closest_distance_squared = float("inf")  # infinity

                for landing_pad in landing_pad_locations:
                    distance_from_waypoint_squared = self.squared_distance(
                        landing_pad, self.waypoint
                    )

                    # update  closest_landing_pad
                    if distance_from_waypoint_squared < closest_distance_squared:
                        closest_distance_squared = distance_from_waypoint_squared
                        self.closest_landing_pad = landing_pad

                # EGDE CASE: landing pad is on the waypoint
                if closest_distance_squared == 0:
                    command = commands.Command.create_land_command()
                    print("Drone is landing directly on the waypoint!")
                else:
                    diff_distance_x = (
                        self.closest_landing_pad.location_x - current_position.location_x
                    )
                    diff_distance_y = (
                        self.closest_landing_pad.location_y - current_position.location_y
                    )
                    command = commands.Command.create_set_relative_destination_command(
                        diff_distance_x, diff_distance_y
                    )
                    print("Moving to closest landing pad!")
        return command
