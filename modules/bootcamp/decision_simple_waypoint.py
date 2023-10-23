"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
import math
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

        # Do something based on the report and the state of this class...
        # Assuming 'commands' and 'drone_status' are imported modules
        # and self.waypoint, report are provided context

        status = report.status
        pos = report.position
        way_x = self.waypoint.location_x
        way_y = self.waypoint.location_y
        rel_dest_x = way_x - pos.location_x
        rel_dest_y = way_y - pos.location_y

        within_range = self.within_range_of(self.waypoint, pos)

        if within_range and status == drone_status.DroneStatus.MOVING:
            command = commands.Command.create_halt_command()
            
        elif within_range and status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_land_command()
            
        elif not within_range and status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_set_relative_destination_command(way_x, way_y)
            
        elif status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_set_relative_destination_command(rel_dest_x, rel_dest_y)

        
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def within_range_of(self, l1: location.Location, l2: location.Location):
        distance = math.sqrt((l1.location_x - l1.location_x)**2 + (l1.location_y - l2.location_x)**2)
        return distance < self.acceptance_radius
    