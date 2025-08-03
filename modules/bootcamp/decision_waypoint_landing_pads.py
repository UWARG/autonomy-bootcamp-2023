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

        # Add your own
        self.reached_waypoint = False

        self.dist_to_landing_pad = float("inf")

        self.closest_pad = None

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

        # Do something based on the report and the state of this class...
        # Calculate distance

        def distance_squared(a: location.Location, b: location.Location) -> float:
            return (a.location_x - b.location_x) ** 2 + (a.location_y - b.location_y) ** 2

        distance_to_waypoint = distance_squared(self.waypoint, report.position)

        # Halted Start
        if report.status == drone_status.DroneStatus.HALTED:
            # If waypoint reached
            if distance_to_waypoint <= self.acceptance_radius**2 and not self.reached_waypoint:
                # Find Closest Pad
                for pad in landing_pad_locations:
                    if (
                        distance_squared(
                            pad,
                            report.position,
                        )
                        < self.dist_to_landing_pad
                    ):
                        self.dist_to_landing_pad = distance_squared(
                            pad,
                            report.position,
                        )
                        self.closest_pad = pad
                # Move to closest pad
                x = self.closest_pad.location_x - report.position.location_x
                y = self.closest_pad.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(x, y)
                self.reached_waypoint = True
            # Land if pad reached
            elif self.reached_waypoint:
                if (
                    distance_squared(
                        self.closest_pad,
                        report.position,
                    )
                    <= self.acceptance_radius**2
                ):
                    command = commands.Command.create_land_command()
            # Move towards waypoint
            else:
                x = self.waypoint.location_x - report.position.location_x
                y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(x, y)
        # Moving
        elif report.status == drone_status.DroneStatus.MOVING:
            # Stop if waypoint reached
            if not self.reached_waypoint:
                if distance_to_waypoint <= self.acceptance_radius**2:
                    command = commands.Command.create_halt_command()
            # Stop if pad reached
            else:
                if distance_squared(self.closest_pad, report.position) <= self.acceptance_radius**2:
                    command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
