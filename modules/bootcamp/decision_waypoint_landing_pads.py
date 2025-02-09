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
        self.has_sent_landing_command = False
        self.passed_waypoint = False
        self.counter = 0
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
        if self.counter == 0:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x,
                self.waypoint.location_y - report.position.location_y,
            )
        if report.status == drone_status.DroneStatus.HALTED:
            if self.passed_waypoint:
                closest_dist_x = float("inf")
                closest_dist_y = float("inf")
                closest_dist = closest_dist_x**2 + closest_dist_y**2

                for pad in landing_pad_locations:
                    dist = ((report.position.location_x - pad.location_x) ** 2) + (
                        (report.position.location_x - pad.location_x) ** 2
                    )
                    if closest_dist > dist:
                        closest_dist = dist
                        closest_dist_x = pad.location_x
                        closest_dist_y = pad.location_y

                if ((report.position.location_x - closest_dist_x) ** 2) + (
                    (report.position.location_y - closest_dist_y) ** 2
                ) < self.acceptance_radius**2:
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        closest_dist_x - report.position.location_x,
                        closest_dist_y - report.position.location_y,
                    )
            else:
                if ((report.position.location_x - self.waypoint.location_x) ** 2) + (
                    (report.position.location_y - self.waypoint.location_y) ** 2
                ) < self.acceptance_radius**2:
                    closest_dist_x = float("inf")
                    closest_dist_y = float("inf")
                    closest_dist = closest_dist_x**2 + closest_dist_y**2

                    for pad in landing_pad_locations:
                        dist = ((report.position.location_x - pad.location_x) ** 2) + (
                            (report.position.location_x - pad.location_x) ** 2
                        )
                        if closest_dist > dist:
                            closest_dist = dist
                            closest_dist_x = pad.location_x
                            closest_dist_y = pad.location_y
                    command = commands.Command.create_set_relative_destination_command(
                        closest_dist_x - report.position.location_x,
                        closest_dist_y - report.position.location_y,
                    )
                    self.passed_waypoint = True
                else:  # stopped unexpectedly
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y,
                    )
        self.counter += 1

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
