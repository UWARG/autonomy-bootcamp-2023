"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


import math
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
    @staticmethod
    def calculate_distance(loc1: location.Location, loc2: location.Location) -> float:
        return ((loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2) ** 0.5
    @staticmethod
    def calculate_direction(from_loc: location.Location, to_loc: location.Location) -> location.Location:
        """
        Calculate the direction vector from current location to waypoint.
        """
        direction_x = to_loc.location_x - from_loc.location_x
        direction_y = to_loc.location_y - from_loc.location_y
        return location.Location(location_x=direction_x, location_y=direction_y)

    
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius
        self.has_started_journey = False
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
        distance = DecisionSimpleWaypoint.calculate_distance(report.position, self.waypoint)
        
        if report.status == drone_status.DroneStatus.HALTED:

            fly_direction = DecisionSimpleWaypoint.calculate_direction(report.position, self.waypoint) 
            if distance <= self.acceptance_radius:
                print("Arrived, Prepare to land")
                self.has_started_journey = False
                return commands.Command.create_land_command()
            elif not self.has_started_journey:
                print("Haven't started yet, Prepare to start journey")
                self.has_started_journey = True
                return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
            else:
                print('Unexpected halted situation, resume movement')
                return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
            
        if report.status == drone_status.DroneStatus.MOVING and distance <= self.acceptance_radius:
            print('Reaches acceptance_radius, halt the drone')
            return commands.Command.create_halt_command()
                
          
        # Do something based on the report and the state of this class...

        # Remove this when done
       
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command

    




