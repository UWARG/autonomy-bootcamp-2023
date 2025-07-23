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
        self.has_reached_waypoint = False
        self.has_sent_landing_command = False
        self.closest_landing_pad = None

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

    @staticmethod
    def distance_between_locations_squared(
        location_1: location.Location, location_2: location.Location
    ) -> float:
        """
        Calculate the distance between two locations, does not use square root.
        """
        return (location_1.location_x - location_2.location_x) ** 2 + (
            location_1.location_y - location_2.location_y
        ) ** 2

    def find_closest_landing_pad(
        self, drone_pos: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> None:
        """
        Find the closest landing pad to the drone's current position.
        """
        if self.closest_landing_pad is None:
            min_distance_squared = float("inf")
            closest = None
            for landing_pad in landing_pad_locations:
                distance_to_landing_pad_squared = self.distance_between_locations_squared(
                    drone_pos, landing_pad
                )
                if distance_to_landing_pad_squared < min_distance_squared:
                    min_distance_squared = distance_to_landing_pad_squared
                    closest = landing_pad
            self.closest_landing_pad = closest

    def within_acceptance_radius(
        self, drone_pos: location.Location, target_location: location.Location
    ) -> bool:
        """
        Check if the drone is within the acceptance radius of the target location.
        """
        distance_squared = self.distance_between_locations_squared(drone_pos, target_location)
        return distance_squared <= self.acceptance_radius**2

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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
        drone_x = report.position.location_x
        drone_y = report.position.location_y
        drone_pos = report.position

        waypoint_x = self.waypoint.location_x
        waypoint_y = self.waypoint.location_y

        # Decide target
        if self.closest_landing_pad is None:
            target_x = waypoint_x
            target_y = waypoint_y
        else:
            target_x = self.closest_landing_pad.location_x
            target_y = self.closest_landing_pad.location_y

        # Only act if drone is halted
        if report.status == drone_status.DroneStatus.HALTED:
            # If we haven't reached the waypoint yet, check against waypoint
            if not self.has_reached_waypoint:
                distance_squared = (waypoint_x - drone_x) ** 2 + (waypoint_y - drone_y) ** 2
                within_acceptance_radius = distance_squared <= self.acceptance_radius**2
                if within_acceptance_radius:
                    self.has_reached_waypoint = True
                    self.find_closest_landing_pad(drone_pos, landing_pad_locations)
                    target_x = self.closest_landing_pad.location_x
                    target_y = self.closest_landing_pad.location_y
                    # Move to landing pad after reaching waypoint
                    print(
                        f"Waypoint reached. Moving to closest landing pad at: ({target_x}, {target_y})"
                    )
                    command = commands.Command.create_set_relative_destination_command(
                        target_x - drone_x,
                        target_y - drone_y,
                    )
                else:
                    # Still traveling to waypoint
                    command = commands.Command.create_set_relative_destination_command(
                        waypoint_x - drone_x,
                        waypoint_y - drone_y,
                    )
            # If we have reached the waypoint, check against landing pad
            elif not self.has_sent_landing_command:
                distance_squared = (target_x - drone_x) ** 2 + (target_y - drone_y) ** 2
                within_acceptance_radius = distance_squared <= self.acceptance_radius**2
                if within_acceptance_radius:
                    print("Within acceptance radius of landing pad, sending landing command.")
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        target_x - drone_x,
                        target_y - drone_y,
                    )
        return command
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
