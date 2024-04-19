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
        self.radius_squared = self.acceptance_radius**2
        self.reached_way_point = False
        self.to_land_at = None

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

        if self.reached_way_point:
            dist_squared = (self.to_land_at.location_x - report.position.location_x)**2 + (self.to_land_at.location_y - report.position.location_y)**2
        else:
            dist_squared = (self.waypoint.location_x - report.position.location_x)**2 + (self.waypoint.location_y - report.position.location_y)**2

        # Do something based on the report and the state of this class...
        if dist_squared <= self.radius_squared:
            if self.reached_way_point and report.status == drone_status.DroneStatus.HALTED:
                command = commands.Command.create_land_command()
            else:
                self.reached_way_point = True
                minimum_distance = float("inf")

                # Iterate through landing pad locations to find closest
                for landing_pad in landing_pad_locations:
                    distance = self.distance_squared_calculator(report.position, landing_pad)
                    if distance < minimum_distance:
                        minimum_distance = distance
                        self.to_land_at = landing_pad
                command = commands.Command.create_halt_command()
        elif report.status == drone_status.DroneStatus.HALTED:
            if self.reached_way_point:
                command = commands.Command.create_set_relative_destination_command(self.to_land_at.location_x - report.position.location_x, self.to_land_at.location_y - report.position.location_y)
            else:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)            

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    def distance_squared_calculator(self, start: location.Location, end: location.Location) -> float:
        """
        Calculates the squared value of the distance between two points
        """
        return (end.location_x - start.location_x)**2 + (end.location_y - start.location_y)**2
