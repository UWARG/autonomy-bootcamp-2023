"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""
# Disable for bootcamp use
# pylint: disable=unused-import
import sys
from numpy import sqrt
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
        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command( waypoint.location_x,  waypoint.location_y)
        ]
        self.has_sent_landing_command = False
        self.found_closest_landing_pad = False
        self.landed = False

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    def closest_pad(self, current, pads):
        smallest_distance, closest_pad = float('inf'), None

        for pad in pads:
            distance = self.calculate_distance(pad.location_x, pad.location_y, current.location_x, current.location_y)
            if distance < smallest_distance:
                smallest_distance, closest_pad = distance, pad
        
        return closest_pad

    def calculate_distance(self, x1, y1, x2, y2):
        dx = x2-x1
        dy = y2-y1
        return sqrt((dx**2)+(dy**2))

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

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(self.commands): #Fly to waypoint
            command = self.commands[self.command_index]
            self.command_index+=1

        elif report.status == drone_status.DroneStatus.HALTED and not self.found_closest_landing_pad: # Fly to closest landing pad
            closest_pad = self.closest_pad(report.position,landing_pad_locations)

            if closest_pad is not None:
                command = commands.Command.create_set_relative_destination_command(
                    closest_pad.location_x - report.position.location_x,
                    closest_pad.location_y - report.position.location_y
                )
                self.found_closest_landing_pad = True
        
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command: # Land
            command = commands.command.create_land_command()
            self.has_sent_landing_command = True
        
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        # Remove this when done

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
