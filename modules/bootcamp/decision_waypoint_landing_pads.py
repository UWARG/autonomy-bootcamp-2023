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
import math

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
        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y),
     
        ]
        self.has_sent_landing_command = False

        self.counter = 0

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        This method will be called in an infinite loop.
        """
        # Default command
        command = commands.Command.create_null_command()

        # Helper functions
        def check_radius(current_x, current_y, target_x, target_y, radius):
            """Check if the current position is within a specified radius of the target."""
            return math.sqrt((target_x - current_x) ** 2 + (target_y - current_y) ** 2) <= radius

        def calculate_distance(loc1, loc2):
            """Calculate the Euclidean distance between two Location objects."""
            return math.sqrt((loc2.location_x - loc1.location_x) ** 2 + (loc2.location_y - loc1.location_y) ** 2)

        def find_closest_landing_pad(drone_position, landing_pads):
            """Find the closest landing pad from the drone's current position."""
            closest_pad = None
            min_distance = float('inf')
            for pad in landing_pads:
                distance = calculate_distance(drone_position, pad)
                if distance < min_distance:
                    min_distance = distance
                    closest_pad = pad
            return closest_pad

        # Step 1: Navigate to the waypoint
        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(self.commands):
            print(f"Halted at: {report.position}")

            # Issue the next movement command towards the waypoint
            command = self.commands[self.command_index]
            self.command_index += 1

        # Step 2: Check if the drone is at the waypoint
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            # If the drone is close enough to the waypoint, find the closest landing pad
            if check_radius(
                report.position.location_x, report.position.location_y,
                self.waypoint.location_x, self.waypoint.location_y, self.acceptance_radius
            ):
                # Find the closest landing pad
                closest_pad = find_closest_landing_pad(report.position, landing_pad_locations)

                # Check if the drone is within landing range of the closest pad
                if check_radius(
                    report.position.location_x, report.position.location_y,
                    closest_pad.location_x, closest_pad.location_y, self.acceptance_radius
                ):
                    # Land at the closest landing pad
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
                    
                else:
                    # Move towards the closest landing pad if not already there
                    command = commands.Command.create_set_relative_destination_command(
                        closest_pad.location_x - report.position.location_x,
                        closest_pad.location_y - report.position.location_y
                    )

        # Increment counter for tracking run calls
        self.counter += 1

        return command
