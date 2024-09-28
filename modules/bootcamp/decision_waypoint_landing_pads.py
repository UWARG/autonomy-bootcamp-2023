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
import math


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

        self.has_sent_landing_command = False

        self.has_sent_fly_to_waypoint_command = False

        self.has_sent_fly_to_landingpad_command = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
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
            report.status == drone_status.DroneStatus.HALTED
            and not self.has_sent_fly_to_waypoint_command
        ):
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
            self.has_sent_fly_to_waypoint_command = True
        elif (
            report.status == drone_status.DroneStatus.HALTED
            and not self.has_sent_fly_to_landingpad_command
        ):
            shortest_distance = 100000
            nearest_landingpad = location.Location(0, 0)

            for i in range(0, len(landing_pad_locations)):
                distance = math.sqrt(
                    pow(landing_pad_locations[i].location_x, 2)
                    + pow(landing_pad_locations[i].location_y, 2)
                )
                if shortest_distance > distance:
                    shortest_distance = distance
                    nearest_landingpad = landing_pad_locations[i]

            command = commands.Command.create_set_relative_destination_command(
                nearest_landingpad.location_x - self.waypoint.location_x,
                nearest_landingpad.location_y - self.waypoint.location_y,
            )
            self.has_sent_fly_to_landingpad_command = True

        elif (
            report.status == drone_status.DroneStatus.HALTED
            and not self.has_sent_landing_command
        ):
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
