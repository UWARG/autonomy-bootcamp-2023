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
        status = report.status
        relative_x_dist = self.waypoint.location_x - report.position.location_x
        relative_y_dist = self.waypoint.location_y - report.position.location_y

        if status == drone_status.DroneStatus.HALTED:
            # Check if halted at initial position or at waypoint
            if self.relative_distance(relative_x_dist, relative_y_dist) < self.acceptance_radius:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(
                    relative_x_dist,
                    relative_y_dist,
                )
        elif status == drone_status.DroneStatus.MOVING:
            if self.relative_distance(relative_x_dist, relative_y_dist) < self.acceptance_radius:
                command = commands.Command.create_halt_command()

            
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def relative_distance(
            self, 
            relative_x_dist: float, 
            relative_y_dist: float,
            ) -> float:
        return (relative_x_dist ** 2 + relative_y_dist ** 2) ** 0.5