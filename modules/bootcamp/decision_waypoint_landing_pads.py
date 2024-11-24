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
        self.closest_landing_pad = location.Location(0, 0)
        self.reached_waypoint = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def is_same(self, position1: location.Location, position2: location.Location) -> bool:
        """
        Returns True if the two position differ by less than the acceptance radius.
        """
        return (
            abs(position1.location_x - position2.location_x) < self.acceptance_radius
            and abs(position1.location_y - position2.location_y) < self.acceptance_radius
        )

    def find_closest(self, landing_pads: "list[location.Location]") -> None:
        """
        Finds the closest landing pad to the waypoint and stores it in self.
        """
        min_distance = float("inf")
        for pad in landing_pads:
            new_distance = (pad.location_x - self.waypoint.location_x) ** 2 + (
                pad.location_y - self.waypoint.location_y
            ) ** 2
            if new_distance < min_distance:
                self.closest_landing_pad = pad
                min_distance = new_distance

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
        if report.status.name == "HALTED":
            if not self.reached_waypoint:
                # At waypoint.
                if self.is_same(self.waypoint, report.position):
                    print("reached waypoint")
                    self.reached_waypoint = True
                    self.find_closest(landing_pad_locations)
                    print(self.closest_landing_pad)
                    command = commands.Command.create_set_relative_destination_command(
                        self.closest_landing_pad.location_x - report.position.location_x,
                        self.closest_landing_pad.location_y - report.position.location_y,
                    )
                # At origin.
                else:
                    print("should not be here")
                    print(self.waypoint)
                    print(report.position)
                    print(self.is_same(self.waypoint, report.position))
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y,
                    )
            # At landing pad.
            else:
                command = commands.Command.create_land_command()
        elif report.status.name == "MOVING":
            # At waypoint OR waypoint has been reached and at landing pad.
            if self.is_same(self.waypoint, report.position) or (
                self.reached_waypoint and self.is_same(self.closest_landing_pad, report.position)
            ):
                print(self.waypoint)
                print(report.position)
                print(self.is_same(self.waypoint, report.position))
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
