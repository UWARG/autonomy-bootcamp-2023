"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
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

        # Do something based on the report and the state of this class...

        # Get access to ccordinates and desired waypoint
        waypoint = self.waypoint
        current_position = report.position

        distance_horizontal = waypoint.location_x - current_position.location_x
        distance_vertical = waypoint.location_y - current_position.location_y

        squared_distance_to_waypoint = (distance_horizontal**2) + (distance_vertical**2)

        # Compare shortest distance to acceptance radius w/o square roots for computational efficiency
        if squared_distance_to_waypoint <= self.acceptance_radius**2:
            return commands.Command.create_land_command()

        # Handles BONUS: Ensures halted drone moves by relative amount when halted
        if report.status == drone_status.DroneStatus.HALTED:
            return commands.Command.create_set_relative_destination_command(
                distance_horizontal, distance_vertical
            )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
