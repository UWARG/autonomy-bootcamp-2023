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

        self.reached_at_waypoint = False
        self.reached_at_landing_pad = False

        self.the_closest_landing_pad = None
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
        command = commands.Command.create_null_command()
        status = report.status
        halted = drone_status.DroneStatus.HALTED

        if status == halted:
            if not self.reached_at_waypoint:
                relative_x = self.waypoint.location_x - report.position.location_x
                relative_y = self.waypoint.location_y - report.position.location_y

                if (
                    abs(relative_x) < self.acceptance_radius
                    and abs(relative_y) < self.acceptance_radius
                ):
                    self.reached_at_waypoint = True
                    self.the_closest_landing_pad = self.find_closest_landing_pad(
                        report.position, landing_pad_locations
                    )
                    relative_x = (
                        self.the_closest_landing_pad.location_x - report.position.location_x
                    )
                    relative_y = (
                        self.the_closest_landing_pad.location_y - report.position.location_y
                    )
                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )
            else:
                relative_x = self.the_closest_landing_pad.location_x - report.position.location_x
                relative_y = self.the_closest_landing_pad.location_y - report.position.location_y

                if abs(relative_x) < 0.1 and abs(relative_y) < 0.1:
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )

        return command

    def find_closest_landing_pad(
        self, current_position: location.Location, landing_pads: "list[location.Location]"
    ) -> location.Location:
        """
        Finds the closest landing pad to the reference location.
        """
        closest_pad = None
        min_distance_squared = float("inf")
        for pad in landing_pads:
            dx = pad.location_x - current_position.location_x
            dy = pad.location_y - current_position.location_y
            distance_squared = dx**2 + dy**2
            if distance_squared < min_distance_squared:
                min_distance_squared = distance_squared
                closest_pad = pad
        return closest_pad
