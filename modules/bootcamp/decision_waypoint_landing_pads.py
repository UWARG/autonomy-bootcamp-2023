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

        self.acceptance_radius = acceptance_radius
        self.has_moved_to_waypoint = False
        self.has_reached_waypoint = False
        self.closest_landing_pad = None
        self.has_moved_to_landing_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def calculate_distance(
        self, location1: location.Location, location2: location.Location
    ) -> float:
        """
        Calculate the Euclidean distance between two locations.
        """
        dx = location1.location_x - location2.location_x
        dy = location1.location_y - location2.location_y
        return (dx * dx + dy * dy) ** 0.5

    def find_closest_landing_pad(
        self, target_location: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        """
        Find the closest landing pad to the target location.
        """
        if not landing_pad_locations:
            raise ValueError("No landing pads available")

        closest_pad = landing_pad_locations[0]
        min_distance = self.calculate_distance(target_location, closest_pad)

        for landing_pad in landing_pad_locations[1:]:
            distance = self.calculate_distance(target_location, landing_pad)
            if distance < min_distance:
                min_distance = distance
                closest_pad = landing_pad

        return closest_pad

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
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        current_position = report.position

        # Calculate distance to waypoint
        distance_to_waypoint = self.calculate_distance(current_position, self.waypoint)

        if report.status == drone_status.DroneStatus.HALTED:
            # Phase 1: Move to waypoint
            if not self.has_reached_waypoint:
                if distance_to_waypoint <= self.acceptance_radius:
                    # We've reached the waypoint, now find closest landing pad
                    self.has_reached_waypoint = True
                    self.closest_landing_pad = self.find_closest_landing_pad(
                        self.waypoint, landing_pad_locations
                    )
                    print(f"Reached waypoint, closest landing pad: {self.closest_landing_pad}")

                    # Check if the closest landing pad is at the waypoint
                    distance_to_landing_pad = self.calculate_distance(
                        current_position, self.closest_landing_pad
                    )
                    if distance_to_landing_pad <= self.acceptance_radius:
                        # Landing pad is at waypoint, land immediately
                        return commands.Command.create_land_command()
                    # Move to landing pad
                    dx = self.closest_landing_pad.location_x - current_position.location_x
                    dy = self.closest_landing_pad.location_y - current_position.location_y
                    self.has_moved_to_landing_pad = True
                    return commands.Command.create_set_relative_destination_command(dx, dy)
                if not self.has_moved_to_waypoint:
                    # Move to waypoint
                    dx = self.waypoint.location_x - current_position.location_x
                    dy = self.waypoint.location_y - current_position.location_y
                    self.has_moved_to_waypoint = True
                    return commands.Command.create_set_relative_destination_command(dx, dy)

            # Phase 2: Move to landing pad and land
            else:
                if self.closest_landing_pad is not None:
                    distance_to_landing_pad = self.calculate_distance(
                        current_position, self.closest_landing_pad
                    )
                    if distance_to_landing_pad <= self.acceptance_radius:
                        # We're at the landing pad, land the drone
                        return commands.Command.create_land_command()
                    if not self.has_moved_to_landing_pad:
                        # Move to landing pad
                        dx = self.closest_landing_pad.location_x - current_position.location_x
                        dy = self.closest_landing_pad.location_y - current_position.location_y
                        self.has_moved_to_landing_pad = True
                        return commands.Command.create_set_relative_destination_command(dx, dy)

        # Return null command to advance the simulator
        return commands.Command.create_null_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
