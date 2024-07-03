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
def calculate_distance(loc1: location.Location, loc2: location.Location) -> float:
    return math.sqrt((loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2)

def calculate_direction(from_loc: location.Location, to_loc: location.Location) -> location.Location:
        """
        Calculate the direction vector from current location to waypoint.
        """
        direction_x = to_loc.location_x - from_loc.location_x
        direction_y = to_loc.location_y - from_loc.location_y
        return location.Location(location_x=direction_x, location_y=direction_y)

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
        self.has_started_journey = False
    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        current_location = report.position
        distance = calculate_distance(current_location, self.waypoint)
        fly_direction = calculate_direction(current_location, self.waypoint)
        if report.status == drone_status.DroneStatus.HALTED:
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
            
        if report.status == drone_status.DroneStatus.MOVING:
            print('Moving towards the destination')
            return commands.Command.create_null_command()
                
        return commands.Command.create_null_command()   

     

















    # def run(self,
    #         report: drone_report.DroneReport,
    #         landing_pad_locations: "list[location.Location]") -> commands.Command:
    #     current_location = report.position
    #     distance = calculate_distance(current_location, self.waypoint)
    #     # Default command
    #     command = commands.Command.create_null_command()
    #     if report.status == drone_status.DroneStatus.HALTED:
    #         if distance <= self.acceptance_radius:
    #             print("Waypoint reached. Initiating landing.")
    #             self.has_started_journey = False  # Reset for potential future commands
    #             return commands.Command.create_land_command()
            
    #         elif not self.has_started_journey:
    #             # Drone is halted at the initial position, not yet moved.
    #             print("Starting journey towards the waypoint.")
    #             direction_to_move = calculate_direction(current_location, self.waypoint)
    #             self.has_started_journey = True
    #             return commands.Command.create_set_relative_destination_command(direction_to_move.location_x, direction_to_move.location_y)
    #         elif self.has_started_journey:
    #             # Unexpected halt, possibly check if it needs to resume course.
    #             print("Unexpected halt detected, resuming course.")
    #             direction_to_move = calculate_direction(current_location, self.waypoint)
    #             return commands.Command.create_set_relative_destination_command(direction_to_move.location_x, direction_to_move.location_y)
            
    #     # If flying and not within radius, continue to fly towards the waypoint.
    #     if report.status == drone_status.DroneStatus.MOVING:
    #         print("In flight towards waypoint, continuing as planned.")
    #         return commands.Command.create_null_command()

    #     return commands.Command.create_null_command()

