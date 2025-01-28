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

        self.waypoint_reached = False
        self.closest_landing_pad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def sqaure_distance(
        self, start_location: location.Location, final_location: location.Location
    ) -> float:
        """
        Calculate the square distance between two locations.
        """
        return (start_location.location_x - final_location.location_x) ** 2 + (
            start_location.location_y - final_location.location_y
        ) ** 2

    def within_accepted_radius(
        self, start_location: location.Location, final_location: location.Location
    ) -> bool:
        """
        Check if the start location is within the acceptance radius of the final location.
        """
        return self.sqaure_distance(start_location, final_location) < self.acceptance_radius**2

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

            # land the drone if it has reached the waypoint, no more landing pads and is within the acceptance radius
            if (
                self.waypoint_reached
                and self.closest_landing_pad is not None
                and self.within_accepepted_radius(report.position, self.closest_landing_pad)
            ):
                command = commands.Command.create_land_command()

            # move the drone to the waypoint
            elif (
                not self.within_accepepted_radius(report.position, self.waypoint)
                and not self.waypoint_reached
            ):
                distance_x = self.waypoint.location_x - report.position.location_x
                distance_y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(
                    distance_x, distance_y
                )

            # find the next closest landing pad
            else:
                shortest_distance = float("inf")

                for landing_pad in landing_pad_locations:
                    if self.sqaure_distance(report.position, landing_pad) < shortest_distance:
                        shortest_distance = self.sqaure_distance(report.position, landing_pad)
                        self.closest_landing_pad = landing_pad

                if self.closest_landing_pad is not None:
                    command = commands.Command.create_set_relative_destination_command(
                        self.closest_landing_pad.location_x - report.position.location_x,
                        self.closest_landing_pad.location_y - report.position.location_y,
                    )
                elif self.closest_landing_pad is None:
                    command = command.create_halt_command()

                self.waypoint_reached = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
