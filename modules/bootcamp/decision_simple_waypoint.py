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
        self.distance_x = waypoint.location_x
        self.distance_y = waypoint.location_y

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
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

        self.distance_x = self.waypoint.location_x - report.position.location_x
        self.distance_y = self.waypoint.location_y - report.position.location_y

        if report.status is drone_status.DroneStatus.HALTED:
            if self.distance_x > 0.1:
                command = commands.Command.create_set_relative_destination_command(min(60, self.distance_x),  0)
            elif self.distance_x < -0.1:
                command = commands.Command.create_set_relative_destination_command(max(-60, self.distance_x),  0)
            elif self.distance_y > 0.1:
                command = commands.Command.create_set_relative_destination_command(0, min(60, self.distance_y))
            elif self.distance_y < -0.1:
                command = commands.Command.create_set_relative_destination_command(0, max(-60, self.distance_y))
            else:
                command = commands.Command.create_land_command()

        # Do something based on the report and the state of this class...

        # Remove this when done
        #raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
