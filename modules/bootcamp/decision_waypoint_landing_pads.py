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

        # Add your own

        self.waypoint_flag = False 

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    
    def dist_sq_between_locations(self, landing_pad_location: location.Location): 
        distance_x = landing_pad_location.location_x - self.waypoint.location_x
        distance_y = landing_pad_location.location_y - self.waypoint.location_y

        return pow(distance_x, 2) + pow(distance_y, 2)
    
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

     
        
        if report.status == drone_status.DroneStatus.HALTED: 
            current_x = report.position.location_x
            current_y = report.position.location_y

           
            relative_y = self.waypoint.location_y - current_y
            relative_x = self.waypoint.location_x - current_x
          
            radius_sq = pow(relative_y, 2) + pow(relative_x, 2) 

            if radius_sq <= pow(self.acceptance_radius, 2): 
                if self.waypoint_flag == True: 
                    command = commands.Command.create_land_command()
                else: 
                    closest_pad = float('inf')
                    closest_pad_idx = -1 

                    for i, landing_pad_location in enumerate(landing_pad_locations):

                        current_pad = self.dist_sq_between_locations(landing_pad_location)
                        if current_pad < closest_pad: 
                            closest_pad = current_pad
                            closest_pad_idx = i
                    
                    self.waypoint = landing_pad_locations[closest_pad_idx]
                    self.waypoint_flag = True

            else: 
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
            
         
           

        # Remove this when done

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
