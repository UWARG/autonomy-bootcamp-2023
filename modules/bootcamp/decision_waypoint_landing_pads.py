"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        # Pre-compute squared acceptance radius
        self.acceptance_radius_sq = self.acceptance_radius**2
        # Create null variable to store the selected landing pad
        self.landing_pad = None
        # Create variable to check if waypoint has been reached to prevent early stopping
        self.traveled_to_waypoint = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
    @staticmethod
    def _compute_relative_cord(cur_loc: location.Location, dest_loc: location.Location):
        """
        Compute the coordinates in x and y to move relative from cur_loc to dest_loc
        """
        cur_x, cur_y = cur_loc.location_x, cur_loc.location_y
        dest_x, dest_y = dest_loc.location_x, dest_loc.location_y

        rel_x = dest_x - cur_x
        rel_y = dest_y - cur_y

        return (rel_x, rel_y)

    def _radius_check(self, cur_loc: location.Location, dest_loc: location.Location):
        """
        Determine if the current location is within the acceptable radius of the destination location

        #TODO: Figure out documentation style

        cur_loc: Location object of current location
        deet_loc: Location object of destination location

        retuns: True if the current location is in the acceptable region of the destination, False otherwise
        """
        cur_x, cur_y = cur_loc.location_x, cur_loc.location_y
        dest_x, dest_y = dest_loc.location_x, dest_loc.location_y
        # Compute compontents of radius for x and y seperately for clarity
        relative_rad_x = (cur_x - dest_x)**2
        relative_rad_y = (cur_y - dest_y)**2
        relative_rad = relative_rad_x + relative_rad_y
        
        # Compare the squared radius between the cur_loc and dest_loc and squared acceptable radius
        return relative_rad <= self.acceptance_radius_sq
    
    @staticmethod
    def _l2_norm_sq(cur_loc: location.Location, dest_loc: location.Location):
        """
        Compute the squared L2 norm between the current location and destination location
        """
        cur_x, cur_y = cur_loc.location_x, cur_loc.location_y
        dest_x, dest_y = dest_loc.location_x, dest_loc.location_y

        return (cur_x - dest_x)**2 + (cur_y - dest_y)**2
    
    def _create_move_cmnd(self, cur_loc: location.Location, dest_loc: location.Location):
        """
        Helper function to create movement command 
        """
        movement_cords = self._compute_relative_cord(cur_loc, dest_loc)
        
        return commands.Command.create_set_relative_destination_command(*movement_cords)

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
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
            if not self.traveled_to_waypoint:
                # Check if the way point is actually in the acceptable radius first
                within_radius_waypoint = self._radius_check(report.position, self.waypoint)
                # If it is in the sutiable radius, compute the distances to the 
                if within_radius_waypoint:
                    self.traveled_to_waypoint = True
                    # Compute squared l2 norm between waypoint and landing pads
                    # We used square l2 as a common metric to avoid using sqrt
                    distances = [self._l2_norm_sq(self.waypoint, pad) for pad in landing_pad_locations]
                    print(f"Computed distanced: {distances}")
                    # Get the index of the minimum distance
                    min_id = distances.index(min(distances))
                    self.landing_pad = landing_pad_locations[min_id]
                    print(f"Closest landing pad: {self.landing_pad}")
                    # Move to closest landing pad
                    command = self._create_move_cmnd(report.position, self.landing_pad)
                else:
                    # If we are not in a suitable radius for the way point, we need to compute how to get there
                    command = self._create_move_cmnd(report.position, self.waypoint)

            # Compute case given we have traveled to landing pad
            else:
                # We are now checking if we are in suitable distance of the landing pad to adjust for conditions
                within_radius_landing = self._radius_check(report.position, self.landing_pad)
                
                if within_radius_landing:
                    command = commands.Command.create_land_command()
                else:
                    # Move to landing pad if not in acceptance radius
                    command = self._create_move_cmnd(report.position, self.landing_pad)

        elif report.status == drone_status.DroneStatus.MOVING:
            # If we haven't been to waypoint, check if we are in suitable radius of it
            if not self.traveled_to_waypoint:
                within_radius_waypoint = self._radius_check(report.position, self.waypoint)
                if within_radius_waypoint:
                    # Halt at the way point
                    command = commands.Command.create_halt_command()
            else:
                # Check if we are in suitable distance of the landing pad to land
                within_radius_landing = self._radius_check(report.position, self.landing_pad)
                if within_radius_landing:
                    command = commands.Command.create_land_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
