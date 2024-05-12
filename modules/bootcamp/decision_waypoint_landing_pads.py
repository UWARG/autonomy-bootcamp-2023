"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision
import math


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
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
        
    def dist(self, position1: location.Location, position2: location.Location):
        return math.sqrt((position1.x - position2.x)**2 + (position1.y - position2.y)**2)
    
    def nearest_pad(self, current_position: location.Location, landing_pad_locations: "list[location.Location]"):
        nearest_pad = None
        min_distance = 100000000  # Initialize with a large number
        
        for pad_location in landing_pad_locations:
            distance = self.dist(current_position, pad_location)
            if distance < min_distance:
                min_distance = distance
                nearest_pad = pad_location
        
        return nearest_pad
    
    def land(self, landing_pad: location.Location, current_position: location.Location):
        if self.calculate_distance(current_position, landing_pad) < self.acceptance_radius:
            return commands.Command.create_land_command()
        else:
            return commands.Command.create_set_relative_destination(landing_pad.x - current_position.x, landing_pad.y - current_position.y)
        
    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
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

        # Do something based on the report and the state of this class...



        # Remove this when done
        raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
