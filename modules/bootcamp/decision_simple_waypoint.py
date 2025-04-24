"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
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
        # Pre compute squared acceptance radius
        self.acceptance_radius_sq = self.acceptance_radius**2
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def _validate_point(
        point_location: location.Location, region: list = ((-60, -60), (60, 60))
    ) -> bool:
        """
        Validates if a given location lies within a fixed region

        Args:
        point_location: Location object of a given point
        region: Tuple of two co-ordinate Tuples consisting of the bottom left and top right corner of a given square

        Returns: True if the point lies in the given region, False otherwise
        """
        x_min, y_min = region[0]
        x_max, y_max = region[1]
        x, y = point_location.location_x, point_location.location_y

        valid_x = x_min <= x <= x_max
        valid_y = y_min <= y <= y_max

        return valid_x and valid_y

    @staticmethod
    def _compute_relative_cord(cur_loc: location.Location, dest_loc: location.Location) -> tuple:
        """
        Compute the coordinates in x and y to move relative from current_location to destination_location

        Args:
        current_location: Location object of drone's current location
        destination_location: Location object of desired destination

        Returns: Tuple of relative (X, Y) co-ordinates from current location to destination location
        """
        cur_x, cur_y = cur_loc.location_x, cur_loc.location_y
        dest_x, dest_y = dest_loc.location_x, dest_loc.location_y

        rel_x = dest_x - cur_x
        rel_y = dest_y - cur_y

        return (rel_x, rel_y)

    def _radius_check(self, cur_loc: location.Location, dest_loc: location.Location) -> bool:
        """
        Determine if the current location is within the acceptable radius of the destination location

        Args:
        current_location: Location object of current location
        deet_loc: Location object of destination location

        Retuns: True if the current location is in the acceptable region of the destination, False otherwise
        """
        cur_x, cur_y = cur_loc.location_x, cur_loc.location_y
        dest_x, dest_y = dest_loc.location_x, dest_loc.location_y
        # Compute compontents of radius for x and y seperately for clarity
        relative_rad_x = (cur_x - dest_x) ** 2
        relative_rad_y = (cur_y - dest_y) ** 2
        relative_rad = relative_rad_x + relative_rad_y

        # Compare the squared radius between the cur_loc and dest_loc and squared acceptable radius
        return relative_rad <= self.acceptance_radius_sq

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

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
            # Check if drone is in acceptable radius of destination
            within_radius = self._radius_check(report.position, self.waypoint)
            if within_radius:
                # If within radius, send land command
                command = commands.Command.create_land_command()
            else:
                # If not in acceptable radius, initate steps to move to valid destination
                # Move only if destination is valid
                valid_dest = self._validate_point(self.waypoint)
                if valid_dest:
                    # Compute relative distance to travel and provide move command
                    rel_cords = self._compute_relative_cord(report.position, self.waypoint)
                    command = commands.Command.create_set_relative_destination_command(*rel_cords)

        elif report.status == drone_status.DroneStatus.MOVING:
            # Check if drone is proximity of destination
            within_radius = self._radius_check(report.position, self.waypoint)
            if within_radius:
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
