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
        self.landing = False
        self.waypoint_reached = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def get_coords_to(self, 
                      report: drone_report.DroneReport, 
                      waypoint: location.Location):
        
        return (waypoint.location_x - report.position.location_x, 
                waypoint.location_y - report.position.location_y)
    
    
    def coords_to_dist(self, coords: "tuple[float, float]"):
        return ((coords[0]**2) + (coords[1]**2))**0.5
    
    
    def closest_pad(self, 
                    report: drone_report.DroneReport, 
                    pad_locations: "list[location.Location]"):
        
        retval = pad_locations[0]
        retval_dist = self.coords_to_dist(self.get_coords_to(report, retval))

        for i in range(1, len(pad_locations)):
            candidate = pad_locations[i]
            candidate_dist = self.coords_to_dist(self.get_coords_to(report, candidate))

            if candidate_dist < retval_dist:
                retval = candidate
                retval_dist = candidate_dist
        
        return retval


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

        if report.status == drone_status.DroneStatus.HALTED and not self.landing:
            
            if self.coords_to_dist(self.get_coords_to(report, self.waypoint)) < self.acceptance_radius:
                print("I am over something important!!")
                if not self.waypoint_reached:
                    print("I am seeing the waypoint for the first time!!")
                    self.waypoint_reached = True
                    print("About to find closest landing pad!!!")
                    self.waypoint = self.closest_pad(report, landing_pad_locations)
                    print("found closest landing pad!!!")
                    move_x, move_y = self.get_coords_to(report, self.waypoint)
                    print("Got relative coords to landing pad!!!")
                    command = commands.Command.create_set_relative_destination_command(move_x, move_y)
                
                else:
                    print("I think I am over the landing pad!! landing now")
                    command = commands.Command.create_land_command()
                    self.landing = True
            else:
                print("I have stopped for some reason and am not over anything important!!!")
                move_x, move_y = self.get_coords_to(report, self.waypoint)
                command = commands.Command.create_set_relative_destination_command(move_x, move_y)
            


        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
