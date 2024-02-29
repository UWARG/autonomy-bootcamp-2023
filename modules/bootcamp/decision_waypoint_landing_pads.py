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
        
        self.command_index = 0

        self.commands = [
            commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)
        ]

        self.has_sent_landing_command = False
        self.found_landing_pad = False
        
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
    # helper functions
    def get_distance(self, p1: location.Location, p2: location.Location) -> float:
        """
        gets square of distance between two points
        """
        return (p1.location_x - p2.location_x)**2 + (p1.location_y - p2.location_y)**2    

    def get_closest_landing_pad(self, current_pos: location.Location, landing_pad_locations: "list[location.Location]") -> location.Location:
        """
        finds the landing pad closest to waypoint
        """
        closest_distance = float('inf')
        closest_landing_pad = None
        for landing_pad in landing_pad_locations:
            new_distance = self.get_distance(current_pos, landing_pad)
            if new_distance < closest_distance:
                closest_distance = new_distance
                closest_landing_pad = landing_pad
        
        return closest_landing_pad


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
            # move to waypoint
            # print("Halted at start, moving to waypoint: " + str(report.position))
            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.found_landing_pad:
            # calcualte and move to closest landing pad
            # if already on landing pad, ignore 
            self.found_landing_pad = True
            if self.waypoint not in landing_pad_locations:
                # print("Halted at waypoint: " + str(report.position))
                landing_pad = self.get_closest_landing_pad(report.position, landing_pad_locations) 
                command = commands.Command.create_set_relative_destination_command (
                    landing_pad.location_x - report.position.location_x, 
                    landing_pad.location_y - report.position.location_y)
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            # land if distance to landing pad location is wtihin acceptance_radius
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True
            # print("Halted at landing pad: " + str(report.position))        
        
        # Remove this when done
        # raise NotImplementedError
            
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command