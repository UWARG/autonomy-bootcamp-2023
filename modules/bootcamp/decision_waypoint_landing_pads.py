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
        self.acceptance_radius_squared = self.acceptance_radius**2
        # Create null variable to store the selected landing pad
        self.landing_pad = None
        # Create variable to check if waypoint has been reached to prevent early stopping
        self.traveled_to_waypoint = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def _compute_relative_cord(
        current_location: location.Location, destination_location: location.Location
    ) -> tuple:
        """
        Compute the coordinates in x and y to move relative from current_location to destination_location

        Args:
        current_location: Location object of drone's current location
        destination_location: Location object of desired destination

        Returns: Tuple of relative (X, Y) co-ordinates from current location to destination location
        """
        current_x, current_y = current_location.location_x, current_location.location_y
        destination_x, destination_y = (
            destination_location.location_x,
            destination_location.location_y,
        )

        rel_x = destination_x - current_x
        rel_y = destination_y - current_y

        return (rel_x, rel_y)

    @staticmethod
    def _l2_norm_squared(
        current_location: location.Location, destination_location: location.Location
    ) -> float:
        """
        Compute the squared L2 norm between the current location and destination location
        All calculations are done in squared L2 norm to avoid the use of square roots

        Args:
        current_location: Location object of drone's current location
        destination_location: Location object of destination location

        Returns: Float of squared L2 norm between the two distances
        """
        current_x, current_y = current_location.location_x, current_location.location_y
        destination_x, destination_y = (
            destination_location.location_x,
            destination_location.location_y,
        )

        return (current_x - destination_x) ** 2 + (current_y - destination_y) ** 2

    def _generate_move_command(
        self, current_location: location.Location, destination_location: location.Location
    ) -> commands.Command:
        """
        Helper function to create movement command

        Args:
        current_location: Location object of drone's current location
        destination_location: Location object of destination location

        Returns: Command object with movement specified between current location and destinationlocation
        """
        movement_cords = self._compute_relative_cord(current_location, destination_location)

        return commands.Command.create_set_relative_destination_command(*movement_cords)

    def _radius_check(
        self, current_location: location.Location, destination_location: location.Location
    ) -> bool:
        """
        Determine if the current location is within the acceptable radius of the destination location

        Args:
        current_location: Location object of current location
        destination_location: Location object of destination location

        Retuns: True if the current location is in the acceptable region of the destination, False otherwise
        """
        current_x, current_y = current_location.location_x, current_location.location_y
        destination_x, destination_y = (
            destination_location.location_x,
            destination_location.location_y,
        )
        # Compute compontents of radius for x and y seperately for clarity
        relative_radius_x = (current_x - destination_x) ** 2
        relative_radius_y = (current_y - destination_y) ** 2
        relative_radius = relative_radius_x + relative_radius_y

        # Compare the squared radius between the current_location and destination_location and squared acceptable radius
        return relative_radius <= self.acceptance_radius_squared

    def _get_min_location(
        self, current_location: location.Location, list_locations: list[location.Location]
    ) -> location.Location:
        """
        Get the location of the closest landing pad to the current location

        Args:
        current_location: Location object of drone's current location
        list_locations: List of Location objects

        Returns: Location object of location closest to current location
        """
        # Compute squared l2 norm of from current location to all other locations
        distances = [self._l2_norm_squared(current_location, loc) for loc in list_locations]
        print(f"Locations: {list_locations}")
        print(f"distances:{distances}")

        # Get the index of the minimum distance
        min_id = distances.index(min(distances))
        # Return the min location
        return list_locations[min_id]

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
                    # Get closest landing pad to waypoint
                    # print(landing_pad_locations)
                    self.landing_pad = self._get_min_location(self.waypoint, landing_pad_locations)
                    # Move to closest landing pad
                    command = self._generate_move_command(report.position, self.landing_pad)
                else:
                    # If we are not in a suitable radius for the way point, we need to compute how to get there
                    command = self._generate_move_command(report.position, self.waypoint)

            # Compute case given we have traveled to landing pad
            else:
                # We are now checking if we are in suitable distance of the landing pad to adjust for conditions
                within_radius_landing = self._radius_check(report.position, self.landing_pad)

                if within_radius_landing:
                    command = commands.Command.create_land_command()
                else:
                    # Move to landing pad if not in acceptance radius
                    command = self._generate_move_command(report.position, self.landing_pad)

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
                    command = commands.Command.create_halt_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
