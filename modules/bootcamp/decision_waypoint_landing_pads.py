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

        self.reached_waypoint = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
    def pad_distance_squared(self,
                             pad: location.Location, 
                             drone: location.Location) -> float:
        
        return (pad.location_x - drone.location_x) ** 2 + (pad.location_y - drone.location_y) ** 2

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

        distance_x = self.waypoint.location_x - report.position.location_x
        distance_y = self.waypoint.location_y - report.position.location_y

        # If drone is moving, we don't need to do anything
        if report.status is drone_status.DroneStatus.HALTED:
            # If drone has arrived at it's destination
            if abs(distance_x) < 0.1 and abs(distance_y) < 0.1:
                # If it has previously reached the waypoint, it must be at the landing pad
                if self.reached_waypoint:
                    command = commands.Command.create_land_command()
                    return command
                
                # If the drone just arrived at the waypoint
                self.reached_waypoint = True
                closest_pad = landing_pad_locations[0]
                closest_pad_distance_squared = float('inf')
                
                #Find the closest landing pad
                for landing_pad_location in landing_pad_locations:
                    distance_to_pad_squared = self.pad_distance_squared(landing_pad_location, report.position)
                    if distance_to_pad_squared < closest_pad_distance_squared:
                        closest_pad_distance_squared = distance_to_pad_squared
                        closest_pad = landing_pad_location
                
                # Set new waypoint at the closest landing pad
                self.waypoint = closest_pad

            # If drone is halted but has not arrived at it's destination, move to destination
            else:
                command = commands.Command.create_set_relative_destination_command(distance_x, distance_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
