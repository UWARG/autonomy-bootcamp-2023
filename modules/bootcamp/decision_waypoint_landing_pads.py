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

        self.boundary_x, self.boundary_y = 60, 60

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
        
        # Helper function for finding distance
        def distance_squared(start: location.Location, end: location.Location) -> float:
            return (end.location_x-start.location_x)**2 + (end.location_y-start.location_y)**2
        
        # Finding the closest landing pads
        def find_closest_lp(cur_pos: location.Location) -> location.Location:
            closest_lp_loc = landing_pad_locations[0]
            for i in range(1,len(landing_pad_locations)):
                if distance_squared(landing_pad_locations[i], report.position) < distance_squared(closest_lp_loc, report.position):
                    closest_lp_loc = landing_pad_locations[i]
            return closest_lp_loc

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:
            
            # Check if the current position is at the acceptance radius to land
            if distance_squared(report.position, self.waypoint) <= self.acceptance_radius**2:
                command = commands.Command.create_land_command()
            
            # Check if the destination is within the flight boundary
            elif abs(self.waypoint.location_x) <= self.boundary_x and abs(self.waypoint.location_y) <= self.boundary_y:
                delta_x = self.waypoint.location_x - report.position.location_x
                delta_y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(delta_x,delta_y)


        # Remove this when done
        raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
