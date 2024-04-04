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

        self.waypoint_is_landing_pad = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============


    def __distance_squared(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """Returns distance between two locations squared
        """
        return (x2-x1)**2 + (y2-y1)**2
    
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
        
        #If drone is already moving to waypoint do nothing
        if report.status == drone_status.DroneStatus.MOVING:
            return command
               
        if self.__distance_squared(self.waypoint.location_x, self.waypoint.location_y, report.position.location_x, report.position.location_y) > self.acceptance_radius**2 :
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)
        else:
            #If drone has reached landing pad, land
            if self.waypoint_is_landing_pad:
                command = commands.Command.create_land_command()
                return command
            
            #Find closest landing pad
            self.waypoint_is_landing_pad = True
            
            closest_landing_pad_location: location.Location = None
            lowest_distance_squared = float('inf')

            for landing_pad_location in landing_pad_locations:
                new_distance_squared = self.__distance_squared(landing_pad_location.location_x, landing_pad_location.location_y, report.position.location_x, report.position.location_y)

                if new_distance_squared < lowest_distance_squared:
                    closest_landing_pad_location = landing_pad_location
                    lowest_distance_squared = new_distance_squared

            self.waypoint.location_x = closest_landing_pad_location.location_x
            self.waypoint.location_y = closest_landing_pad_location.location_y
            
            command=commands.Command.create_set_relative_destination_command(closest_landing_pad_location.location_x - self.waypoint.location_x, closest_landing_pad_location.location_y - self.waypoint.location_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
