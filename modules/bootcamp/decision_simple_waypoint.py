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
    def need_move(self, report: drone_report.DroneReport):
        if report.status == drone_status.Status.Halted and report.position == report.destination and report.position.distance_to(self.waypoint) > self.acceptance_radius:
            return True
        else:
            return False

    def move(self, report: drone_report.DroneReport):
        x = self.waypoint.x - report.position.x 
        y = self.waypoint.y - report.position.y
        return commands.Command.create_set_relative_destination(x, y)
    
    def at_point(self, report: drone_report.DroneReport):
        if report.status == drone_status.Status.Halted and report.position != report.destination:
            return True
        else:
            return False
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

        # Do something based on the report and the state of this class...
        if self.should_move_to_waypoint(report):
            command = self.move_to_waypoint(report)

        elif self.has_reached_waypoint(report):
            command = commands.Command.create_halt_command()
            
        elif report.status == drone_status.Status.Landed:
            command = commands.Command.create_land_command()
       
        # Remove this when done
        #raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
