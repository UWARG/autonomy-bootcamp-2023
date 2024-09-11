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
        self.commands = commands.Command.create_set_relative_destination_command(
            self.waypoint.location_x, self.waypoint.location_y
        )

        self.has_sent_landing_command = False

        self.min_location = [float("inf"), float("inf")]
        self.starting_halt, self.waypoint_halt = True, True

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

        dist_to_waypoint_x = self.min_location[0] - report.position.location_x
        dist_to_waypoint_y = self.min_location[1] - report.position.location_y
        min_norm = float("inf")

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:
            if self.starting_halt:
                command = self.commands
                self.starting_halt = False

            elif self.waypoint_halt:
                for landing_pads in landing_pad_locations:
                    x, y = (
                        landing_pads.location_x - self.waypoint.location_x,
                        landing_pads.location_y - self.waypoint.location_y,
                    )
                    curr_norm = x**2 + y**2

                    if curr_norm < min_norm:
                        min_norm, self.min_location = curr_norm, (
                            landing_pads.location_x,
                            landing_pads.location_y,
                        )

                command = commands.Command.create_set_relative_destination_command(
                    self.min_location[0] - self.waypoint.location_x,
                    self.min_location[1] - self.waypoint.location_y,
                )
                self.waypoint_halt = False

        if (
            not self.has_sent_landing_command
            and dist_to_waypoint_x**2 + dist_to_waypoint_y**2 <= self.acceptance_radius**2
        ):
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
