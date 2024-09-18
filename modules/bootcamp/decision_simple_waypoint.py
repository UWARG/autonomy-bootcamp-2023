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
        
        # Set initial state
        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(25.0, 25.0)
        ]
        self.has_sent_landing_command = False
        self.reached_destination = False



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
        

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        # Update the current position from the report
        self.current_position = report.position

        # Calculate distance to the waypoint
        distance_to_waypoint = sqrt(
            (self.current_position[0] - self.waypoint.x) ** 2 + (self.current_position[1] - self.waypoint.y) ** 2
        )

        # Check if the drone is within the acceptance radius of the waypoint
        if report.status == "HALTED" and not self.has_sent_landing_command:
            if distance_to_waypoint <= self.acceptance_radius:
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True
            else:
                # Move the drone to the waypoint
                command = self.commands[self.command_index]


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
