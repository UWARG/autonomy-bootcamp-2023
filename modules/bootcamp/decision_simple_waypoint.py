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

        # Add your own

        self.has_sent_landing_command = False

        # Destination coords
        self.destination_x = self.waypoint.location_x
        self.destination_y = self.waypoint.location_y

        self.move_command = commands.Command.create_set_relative_destination_command(
            self.destination_x, self.waypoint.location_y
        )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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

        # Location coords
        location_x = report.position.location_x
        location_y = report.position.location_y

        # Calculate squared distance to waypoint
        distance_x = self.destination_x - location_x
        distance_y = self.destination_y - location_y

        distance_squared = distance_x**2 + distance_y**2
        acceptance_radius_squared = self.acceptance_radius**2

        # Check if the drone should land or move toward the waypoint
        if not self.has_sent_landing_command and report.status == drone_status.DroneStatus.HALTED:

            # If the drone is halted, start the move command
            command = self.commands
            self.has_sent_landing_command = True

        elif distance_squared < acceptance_radius_squared and self.has_sent_landing_command is True:

            # If within acceptance radius and the move command was sent, land the drone
            command = commands.Command.create_land_command()

        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
