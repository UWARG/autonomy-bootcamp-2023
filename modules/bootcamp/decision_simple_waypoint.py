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

        self.upper_flight_bound = 60
        self.lower_flight_bound = -60

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def waypoint_in_bounds(self) -> bool:
        """
        Check to see if the waypoint is within flight bounds

        """
        return (
            self.waypoint.location_x <= self.upper_flight_bound
            and self.waypoint.location_x >= self.lower_flight_bound
            and self.waypoint.location_y <= self.upper_flight_bound
            and self.waypoint.location_y >= self.lower_flight_bound
        )

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

        if self.waypoint_in_bounds():

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
                    command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
