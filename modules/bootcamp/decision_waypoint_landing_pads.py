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
from math import sqrt
import numpy as np

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
        
        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)
        ]
        
        self.reached_waypoint = False
        self.reached_landing_pad = False
        self.has_sent_landing_command = False

        self.counter = 0
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
    def distance_between_2_locations(self, location_pad:location.Location, location_quad:location.Location):
        
        x1 = location_pad.location_x
        y1 = location_pad.location_y
        x2 = location_quad.location_x
        y2 = location_quad.location_y
                
        x_dist = x1-x2
        y_dist = y1-y2
        
        dist = sqrt(pow(x_dist,2) + pow(y_dist,2))
        
        return dist, x_dist, y_dist
    

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

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(self.commands):
            # Print some information for debugging
            print(self.counter)
            print(self.command_index)
            print("Halted at: " + str(report.position))

            command = self.commands[self.command_index]
            self.command_index += 1
        
        elif report.status == drone_status.DroneStatus.HALTED and not self.reached_landing_pad:
            print("Reached waypoint")
            shortest_dist = np.inf
            closest_landing_pad:location.Location = None
            
            for landing_pad in landing_pad_locations:
                dist,_,_ = self.distance_between_2_locations(landing_pad, report.position)        
                if dist<shortest_dist:
                    dist = shortest_dist
                    closest_landing_pad = landing_pad            
            print("Found Closest landing pad: ", closest_landing_pad )
        
            _,x_dist,y_dist = self.distance_between_2_locations(closest_landing_pad, report.position)
            
            command = commands.Command.create_set_relative_destination_command(x_dist, y_dist)
            print(x_dist, y_dist)
            
            self.reached_landing_pad = True
        
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            #Assume a landing pad exists near waypoint within image frame
            command = commands.Command.create_land_command()

            self.has_sent_landing_command = True

        self.counter += 1

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
