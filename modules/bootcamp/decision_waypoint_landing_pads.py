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
        self.reached = False
        self.landing_pad_location = None
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def distance_to_waypoint(self, pos1: location.Location, pos2: location.Location) -> float:
        """
        Calculate the distance between current position and waypoint.
        """
        return ((pos2.location_x - pos1.location_x) ** 2 + 
                (pos2.location_y - pos1.location_y) ** 2)
    
    def best_landing_pad(self, current_position: location.Location, 
                         landing_pad_locations: "list[location.Location]") -> location.Location:
        """
        Calculate the nearest landing pad from the current position.
        """
        best_landing_pad = None
        best_distance = float("inf")
        for landing_pad in landing_pad_locations:
            distance = self.distance_to_waypoint(landing_pad, current_position)
            if distance < best_distance:
                best_distance = distance
                best_landing_pad = landing_pad
        return best_landing_pad
    
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
        if report.status == drone_status.DroneStatus.HALTED:
            if not self.reached:
                distance_to_waypoint_squared = self.distance_to_waypoint(report.position, self.waypoint)
                
                if distance_to_waypoint_squared < self.acceptance_radius**2:
                    self.reached = True
                else:
                    return commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y)
            
            else:
                distance_to_destination_squared = self.distance_to_waypoint(report.position, self.landing_pad_location)
                
                if distance_to_destination_squared < self.acceptance_radius**2:
                    return commands.Command.create_land_command()
                else:
                    best_pad = self.best_landing_pad(report.position, landing_pad_locations)
                    self.landing_pad_location = best_pad

                    return commands.Command.create_set_relative_destination_command(
                        self.landing_pad_location.location_x - report.position.location_x,
                        self.landing_pad_location.location_y - report.position.location_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
