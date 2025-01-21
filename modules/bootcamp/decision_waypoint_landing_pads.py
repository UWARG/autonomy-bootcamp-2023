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
        self.min_flight_bound = -60
        self.max_flight_bound = 60

        self.ready_to_land = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def dist_between(self, final_location: location.Location) -> float:
        """
        Calculate the squared distance between the waypoint and a given location.
        """
        return (self.waypoint.location_x - final_location.location_x) ** 2 + (
            self.waypoint.location_y - final_location.location_y
        ) ** 2

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
        if (
            self.min_flight_bound <= self.waypoint.location_x <= self.max_flight_bound
            and self.min_flight_bound <= self.waypoint.location_y <= self.max_flight_bound
        ):
            distance_from_waypoint = (
                self.waypoint.location_x - report.position.location_x
            ) ** 2 + ((self.waypoint.location_y - report.position.location_y) ** 2)

            if report.status == drone_status.DroneStatus.HALTED:

                if self.ready_to_land:
                    command = commands.Command.create_land_command()

                elif distance_from_waypoint < self.acceptance_radius**2:
                    smallest_distance = float("inf")
                    closest_pad = None

                    for landing_pad in landing_pad_locations:
                        if self.dist_between(landing_pad) < smallest_distance:
                            smallest_distance = self.dist_between(landing_pad)
                            closest_pad = landing_pad

                    if closest_pad is None:
                        command = commands.Command.create_null_command()
                    else:
                        command = commands.Command.create_set_relative_destination_command(
                            (closest_pad.location_x - self.waypoint.location_x),
                            (closest_pad.location_y - self.waypoint.location_y),
                        )

                    self.ready_to_land = True

                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x, self.waypoint.location_y
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
