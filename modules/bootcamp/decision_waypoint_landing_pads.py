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
        self.command_index = 0
        self.commands = [commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)]
        self.finding_landing_pad = False
        self.has_sent_landing_command = False
 
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        
    def distance_between_two_locations_squared(self,location1: location.Location, location2: location.Location) -> float:
        '''
        Finds the distance between two locations squared. Squared in order to avoid the heavily computational square root
        '''
        return (location1.location_x - location2.location_x)**2 + (location1.location_y - location2.location_y)**2
    

    def get_closest_landing_pad(self, current_location: location.Location, landing_pad_locations: "list[location.Location]") -> location.Location:
        '''
        Given the drone's current location (a.k.a waypoint), iterate over the list of landing pad locations to find the closest one
        '''
        closest_landing_pad_location = None
        closest_distance = float('inf')
        for landing_pad_location in landing_pad_locations:
            distance = self.distance_between_two_locations_squared(current_location, landing_pad_location)
            if distance < closest_distance:
                closest_distance = distance
                closest_landing_pad_location = landing_pad_location

        return closest_landing_pad_location


    def get_position_vector(self, position1: location.Location, position2: location.Location) -> "tuple[float,float]":
        '''
        Returns the position vector to go from location 1 to location 2
        '''
        return position2.location_x - position1.location_x, position2.location_y - position1.location_y


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
            # print("Halted at: " + str(report.position))
            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.finding_landing_pad:
            self.finding_landing_pad = True
            if self.waypoint not in landing_pad_locations: #so if this is false, that means the drone is already at a landing pad
                closest_landing_pad = self.get_closest_landing_pad(report.position, landing_pad_locations)
                x, y = self.get_position_vector(report.position, closest_landing_pad)
                command = commands.Command.create_set_relative_destination_command(x, y)
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
