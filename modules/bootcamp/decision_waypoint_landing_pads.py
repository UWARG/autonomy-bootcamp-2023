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
        self.position_x = 0
        self.position_y = 0
        self.reached_waypoint = False

        self.nearest_landing_pad = None
        self.traveling_to_landing_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def find_nearest_landing_pad(self, landing_pad_locations: "list[location.Location]") -> None:
        """
        finds nearest landing pad
        """
        nearest_landing_pad_distance = float("inf")
        nearest_landing_pad = landing_pad_locations[0]

        for landing_pad in landing_pad_locations:
            distance = (landing_pad.location_x - self.position_x) ** 2 + (
                landing_pad.location_y - self.position_y
            ) ** 2

            if distance == 0:
                nearest_landing_pad_distance = 0
                self.nearest_landing_pad = self.waypoint

            if distance < nearest_landing_pad_distance**2:
                nearest_landing_pad_distance = distance
                nearest_landing_pad = landing_pad

        self.nearest_landing_pad = nearest_landing_pad

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

        # Do something based on the report and the state of this class...
        def within_acceptance_radius() -> bool:
            return (
                abs(self.waypoint.location_x - self.position_x) <= self.acceptance_radius
                and abs(self.waypoint.location_y - self.position_y) <= self.acceptance_radius
            )

        def reached_landing_pad() -> bool:
            return (
                abs(self.nearest_landing_pad.location_x - self.position_x) <= self.acceptance_radius
                and abs(self.nearest_landing_pad.location_y - self.position_y)
                <= self.acceptance_radius
            )

        self.position_x = report.position.location_x
        self.position_y = report.position.location_y
        self.reached_waypoint = within_acceptance_radius()

        if not self.traveling_to_landing_pad:
            if report.status == drone_status.DroneStatus.HALTED and not self.reached_waypoint:
                print("Heading to WAYPOINT")
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - self.position_x,
                    self.waypoint.location_y - self.position_y,
                )

            elif report.status == drone_status.DroneStatus.MOVING and self.reached_waypoint:
                print("Reached WAYPOINT")
                command = commands.Command.create_halt_command()

            elif report.status == drone_status.DroneStatus.HALTED and self.reached_waypoint:
                self.traveling_to_landing_pad = True

                self.find_nearest_landing_pad(landing_pad_locations)
                print(self.nearest_landing_pad)

                print("Drone Heading to Landing Pad")
                command = commands.Command.create_set_relative_destination_command(
                    self.nearest_landing_pad.location_x - self.position_x,
                    self.nearest_landing_pad.location_y - self.position_y,
                )
        else:
            if report.status == drone_status.DroneStatus.HALTED and reached_landing_pad():
                print("Landing at LANDING PAD")
                command = commands.Command.create_land_command()

            elif report.status == drone_status.DroneStatus.MOVING and reached_landing_pad():
                print("Drone reached Landing Pad")
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
