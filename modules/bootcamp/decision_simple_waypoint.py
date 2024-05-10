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
        self.commands =[commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y),
                        commands.Command.create_land_command(),
                        commands.Command.create_halt_command()]
        self.to_destination = False
        self.at_boundary = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    def get_position_radius(self, dron_position: "location.Location", waypoint_position: "location.Location") -> float:
            return (dron_position.location_x - waypoint_position.location_x) ** 2 + (dron_position.location_y - waypoint_position.location_y) ** 2
    
    
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
        if report.status == drone_status.DroneStatus.HALTED and not self.to_destination:
            command = self.commands[0]
            self.to_destination = True
        elif report.status == drone_status.DroneStatus.HALTED and (self.get_position_radius(report.position, self.waypoint) <= (self.acceptance_radius ** 2)):
            command = self.commands[1]
        elif report.status == drone_status.DroneStatus.HALTED and (self.get_position_radius(report.position, self.waypoint) >= (self.acceptance_radius ** 2)):
            command = self.commands[0]
        # Remove this when done
        #raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
