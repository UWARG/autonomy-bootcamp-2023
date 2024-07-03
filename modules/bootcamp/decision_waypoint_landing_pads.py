"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
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
def calculate_closest_location(start_loc: location.Location, loc_list:"list[location.Location]") -> location.Location:
    shortest = float('inf')
    
    for landing_loc in loc_list:
        if calculate_distance(start_loc, landing_loc) < shortest:
            shortest = calculate_distance(start_loc, landing_loc)
            shortest_location = landing_loc
    
    return shortest_location



def calculate_distance(loc1: location.Location, loc2: location.Location) -> float:
    return math.sqrt((loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2)

def calculate_direction(from_loc: location.Location, to_loc: location.Location) -> location.Location:
        """
        Calculate the direction vector from current location to waypoint.
        """
        direction_x = to_loc.location_x - from_loc.location_x
        direction_y = to_loc.location_y - from_loc.location_y
        return location.Location(location_x=direction_x, location_y=direction_y)

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
        self.has_started_journey = False
        self.has_reached_waypoint = False
        self.location_closest_landing = 0

      

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        current_location = report.position
        distance_to_waypoint = calculate_distance(current_location, self.waypoint)
        fly_direction = calculate_direction(current_location, self.waypoint)
        if self.has_reached_waypoint:
            distance_to_landing_pad = calculate_distance(current_location, self.location_closest_landing)
            if distance_to_landing_pad <= self.acceptance_radius:
                return commands.Command.create_land_command()
        else:
            if report.status == drone_status.DroneStatus.HALTED and not self.has_reached_waypoint:
                if distance_to_waypoint <= self.acceptance_radius:

                    print("Reached Waypoint, Start journey to closest landing pad")
                    self.has_started_journey = False
                    self.has_reached_waypoint = True
                    self.location_closest_landing = calculate_closest_location(self.waypoint, landing_pad_locations)
                    fly_direction = calculate_direction(current_location, self.location_closest_landing)
                    return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
                elif not self.has_started_journey:
                    print("Haven't started yet, Prepare to start journey")
                    self.has_started_journey = True
                    return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
                else:
                    print('Unexpected halted situation, resume movement')
                    return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
       
        if report.status == drone_status.DroneStatus.MOVING:
                    print('Moving towards the destination')
                    return commands.Command.create_null_command()
       
                    
        return commands.Command.create_null_command()  
       
