"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""
# Disable for bootcamp use
# pylint: disable=unused-import



from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location  # Import your Location class
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
        self.acceptance_radius = acceptance_radius
        
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own
        
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def distance(self, report: drone_report.DroneReport) -> float:
        return ((self.waypoint.location_x - report.position.location_x) ** 2 + (self.waypoint.location_y - report.position.location_y) ** 2) ** 0.5
    
    def need_move(self, report: drone_report.DroneReport) -> bool:
        return self.distance(report) > self.acceptance_radius

    def move(self, report: drone_report.DroneReport) -> commands.Command:
        x = self.waypoint.location_x - report.position.location_x
        y = self.waypoint.location_y - report.position.location_y
        return commands.Command.create_set_relative_destination_command(x, y)

    def at_point(self, report: drone_report.DroneReport) -> bool:
        return report.status == drone_status.DroneStatus.HALTED

    def run(self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]") -> commands.Command:
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
        if self.at_point(report):
            if self.need_move(report):
                command = self.move(report)
            else:
                command = commands.Command.create_land_command()

        elif report.status == drone_status.DroneStatus.MOVING:
            if not self.need_move(report):
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
