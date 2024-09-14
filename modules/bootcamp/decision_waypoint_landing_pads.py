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
        # set as closest landing to waypoint
        self.has_sent_landing_command = False
        self.halt_at_initialization = True
        self.is_halt_at_waypoint = False
        self.closest_pad = location.Location
        self.shortest_distance = [float("inf"), float("inf")]
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
        def square(number) -> float:
            return number**2

        def squared_distance_from_position(point, current_position) -> float:
            distance = square(point.location_x - current_position.location_x) + (
                square(point.location_y - current_position.location_y)
            )
            return distance

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:

            if self.halt_at_initialization:

                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x, self.waypoint.location_y
                )
                self.halt_at_initialization = False
                self.is_halt_at_waypoint = True

            elif self.is_halt_at_waypoint:
                for landing_pad in landing_pad_locations:

                    if (
                        squared_distance_from_position(landing_pad, self.waypoint)
                        < self.shortest_distance[0] ** 2 + self.shortest_distance[1] ** 2
                    ):

                        self.shortest_distance[0], self.shortest_distance[1] = (
                            landing_pad.location_x - report.position.location_x,
                            landing_pad.location_y - report.position.location_y,
                        )
                        self.closest_pad = landing_pad

                command = commands.Command.create_set_relative_destination_command(
                    self.shortest_distance[0], self.shortest_distance[1]
                )
                self.is_halt_at_waypoint = False

            elif (report.position.location_x**2 + report.position.location_y**2) / (
                self.closest_pad.location_x**2 + self.closest_pad.location_y**2
            ) <= (
                (1 + self.acceptance_radius) ** 2
            ):  # checks if current position is in acceptable radius of landing pad by making them a ratio

                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
