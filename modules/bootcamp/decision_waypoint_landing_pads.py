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

        self.has_sent_move_command_to_waypoint = False
        self.has_sent_move_command_to_landing_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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

        if report.status == drone_status.DroneStatus.HALTED:
            # Drone is halted, either in start state, finished moving to waypoint or finished moving to landing pad
            if self.has_sent_move_command_to_landing_pad:
                # Final state after arriving at landing pad
                command = commands.Command.create_land_command()

            if self.has_sent_move_command_to_waypoint and not self.has_sent_move_command_to_landing_pad:
                # State after arriving at waypoint
                closest_landing_pad = self.find_closest_landing_pad(self.waypoint, landing_pad_locations)
                relative_x, relative_y = self.calculate_relative_difference(
                    destination=closest_landing_pad, starting_point=report.position)
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
                self.has_sent_move_command_to_landing_pad = True

            if not self.has_sent_move_command_to_waypoint:
                # Start State - Drone is halted and we have not issued the command to move to waypoint yet
                relative_x, relative_y = self.calculate_relative_difference(
                    destination=self.waypoint, starting_point=report.position)
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
                self.has_sent_move_command_to_waypoint = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command


    def calculate_relative_difference(self, 
                                    destination: location.Location, 
                                    starting_point: location.Location) -> (float, float):
        """
        Given the absolute location of the waypoint and the drone, return the relative distance of the two
        """
        return (destination.location_x - starting_point.location_x, 
                destination.location_y - starting_point.location_y)
    
    def calculate_squared_euclidian_distance(self,
                                     destination: location.Location,
                                     starting_point: location.Location
                                     ) -> float:
        """
        Given two locations, return the euclidian distance of the two
        """
        distance_x, distance_y = self.calculate_relative_difference(destination, starting_point)
        return distance_x ** 2 + distance_y ** 2
    
    def find_closest_landing_pad(self, 
                                 waypoint: location.Location, 
                                 landing_pad_locations: "list[location.Location]") -> location.Location:
        if len(landing_pad_locations) == 0:
            raise ValueError

        closest_landing_pad = min(landing_pad_locations, 
                                  key=lambda location: self.calculate_squared_euclidian_distance(location, self.waypoint))
        
        return closest_landing_pad
