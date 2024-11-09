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
    Travel to the designated waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        self.is_moving_to_waypoint = True
        self.waypoint_reached = False
        self.has_sent_landing_command = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def calculate_distance(self, loc1: location.Location, loc2: location.Location) -> float:
        """Calculate the Euclidean distance between two Location objects.

        Args:
            loc1 (location.Location): The first location.
            loc2 (location.Location): The second location.

        Returns:
            float: The squared Euclidean distance between loc1 and loc2.
        """
        dx = loc2.location_x - loc1.location_x
        dy = loc2.location_y - loc1.location_y
        return dx * dx + dy * dy

    def find_closest_landing_pad(
        self, drone_position: location.Location, landing_pads: "list[location.Location]"
    ) -> location.Location:
        """Find the closest landing pad to the drone's current position.

        Args:
            drone_position (location.Location): The current position of the drone.
            landing_pads (list[location.Location]): A list of possible landing pads.

        Returns:
            location.Location: The landing pad closest to the drone.
        """
        closest_pad = None
        min_distance = float("inf")
        for pad in landing_pads:
            distance = self.calculate_distance(drone_position, pad)
            if distance < min_distance:
                min_distance = distance
                closest_pad = pad
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
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        if report.status == drone_status.DroneStatus.HALTED:
            drone_position = report.position
            print(f"Drone Status: {report.status}")
            print(f"Drone Position: ({drone_position.location_x}, {drone_position.location_y})")
            print(
                f"Available Landing Pads: {[ (pad.location_x, pad.location_y) for pad in landing_pad_locations ]}"
            )

            if self.is_moving_to_waypoint:
                distance_to_waypoint = self.calculate_distance(drone_position, self.waypoint)
                print(f"Distance to Waypoint: {distance_to_waypoint}")

                if distance_to_waypoint >= self.acceptance_radius:
                    # Move towards the waypoint
                    relative_x = self.waypoint.location_x - drone_position.location_x
                    relative_y = self.waypoint.location_y - drone_position.location_y
                    print(f"Setting relative destination to Waypoint: ({relative_x}, {relative_y})")
                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )
                else:
                    # Waypoint reached
                    self.is_moving_to_waypoint = False
                    self.waypoint_reached = True
                    print("Waypoint reached. Preparing to land at the nearest landing pad.")

            elif not self.has_sent_landing_command:
                closest_pad = self.find_closest_landing_pad(drone_position, landing_pad_locations)
                if closest_pad is None:
                    print("No landing pads available. Remaining idle.")
                    return None  # Remain idle if no landing pads are found

                distance_to_pad = self.calculate_distance(drone_position, closest_pad)
                print(f"Closest Landing Pad: ({closest_pad.location_x}, {closest_pad.location_y})")
                print(f"Distance to Landing Pad: {distance_to_pad}")

                if distance_to_pad <= self.acceptance_radius:
                    # Land at the closest landing pad
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
                    print("Landing command issued.")
                else:
                    # Move towards the closest landing pad
                    relative_x = closest_pad.location_x - drone_position.location_x
                    relative_y = closest_pad.location_y - drone_position.location_y
                    print(
                        f"Setting relative destination to Landing Pad: ({relative_x}, {relative_y})"
                    )
                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
