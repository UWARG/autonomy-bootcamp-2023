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
        self.reached_waypoint = False
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
        
        # Find differences in x and y between 2 locations
        def diff_xy(start: location.Location, end: location.Location):
            return end.location_x - start.location_x, end.location_y - start.location_y
        
        # Finding the closest landing pads
        def find_closest_lp(cur_pos: location.Location) -> location.Location:
            closest_lp_loc = None
            closest_lp_dist_squared = float('inf')
            for lp in landing_pad_locations:
                d =  distance_squared(cur_pos, lp)
                if (d < closest_lp_dist_squared) and (abs(lp.location_x) <= self.boundary_x and abs(lp.location_y) <= self.boundary_y):
                    closest_lp_loc = lp
                    closest_lp_dist_squared = d
            return closest_lp_loc

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:
            
            # Check if the current position is at the acceptance radius to land
            if distance_squared(report.position, self.waypoint) <= self.acceptance_radius**2 and not self.reached_waypoint:
                self.reached_waypoint = True # Reached waypoint, now find closest LP to land
            
            # Check if the destination is within the flight boundary
            elif abs(self.waypoint.location_x) <= self.boundary_x and abs(self.waypoint.location_y) <= self.boundary_y and not self.reached_waypoint:
                delta_x, delta_y = diff_xy(report.position, self.waypoint)
                command = commands.Command.create_set_relative_destination_command(delta_x,delta_y)
            
            # If reached waypoint, find shortest LP to land
            elif self.reached_waypoint:
                closest_lp_loc = find_closest_lp(report.position)

                if distance_squared(report.position, closest_lp_loc) <= self.acceptance_radius**2:
                    command = commands.Command.create_land_command()

                else:
                    delta_x, delta_y = diff_xy(report.position, closest_lp_loc)
                    command = commands.Command.create_set_relative_destination_command(delta_x,delta_y)

        # Remove this when done

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
