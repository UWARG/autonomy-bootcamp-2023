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
        self.waypoint_visited: bool = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============


    def __distance_squared(self, a: location.Location, b: location.Location) -> float:
        """Returns distance between two locations squared
        """
        return (b.location_x-a.location_x)**2 + (b.location_y-a.location_y)**2
    
    def __find_closest_landing_pad(self, landing_pad_locations: "list[location.Location]", position: location.Location) -> location.Location:
        """Returns the closest landing pad to the drone
        """
        closest_landing_pad_location: location.Location = None
        lowest_distance_squared = float('inf')

        for landing_pad_location in landing_pad_locations:
            new_distance_squared = self.__distance_squared(landing_pad_location, position)

            if new_distance_squared < lowest_distance_squared:
                closest_landing_pad_location = landing_pad_location
                lowest_distance_squared = new_distance_squared

        return closest_landing_pad_location
    
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
            destination: location.Location = self.waypoint # where the drone should be going
            
            if self.waypoint_visited:
                destination = self.__find_closest_landing_pad(landing_pad_locations, report.position)

            if self.__distance_squared(destination,report.position) < self.acceptance_radius**2:
                if not self.waypoint_visited:
                    self.waypoint_visited = True
                else:
                    command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(destination.location_x - report.position.location_x, destination.location_y - report.position.location_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
