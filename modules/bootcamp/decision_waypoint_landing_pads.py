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
        self.reachedWaypoint = False
        self.padx = 0
        self.pady = 0

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def get_nearest_landing(
        self, position: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> list[float]:
        nearest_pad = None
        for pad in landing_pad_locations:
            dx = pad.location_x - position.location_x
            dy = pad.location_y - position.location_y
            distance = (dx) ** 2 + (dy) ** 2
            if nearest_pad == None:
                nearest_pad = [pad.location_x, pad.location_y]
            elif distance < (nearest_pad[0] ** 2 + nearest_pad[1] ** 2):
                nearest_pad = [pad.location_x, pad.location_y]
        return nearest_pad

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

        position = report.position
        waypoint = self.waypoint
        status = report.status

        distance_from_waypoint_x = waypoint.location_x - position.location_x
        distance_from_waypoint_y = waypoint.location_y - position.location_y

        nearest_pad = None

        if not self.reachedWaypoint:
            if status == drone_status.DroneStatus.HALTED:
                if (
                    distance_from_waypoint_x <= self.acceptance_radius
                    and distance_from_waypoint_y <= self.acceptance_radius
                ):
                    self.reachedWaypoint = True
                    nearest_pad = self.get_nearest_landing(position, landing_pad_locations)
                    self.padx = nearest_pad[0]
                    self.pady = nearest_pad[1]
                    print("finding pads...", nearest_pad)
                elif abs(waypoint.location_x) <= 60 and abs(waypoint.location_y) <= 60:
                    command = commands.Command.create_set_relative_destination_command(
                        distance_from_waypoint_x, distance_from_waypoint_y
                    )
            elif status == drone_status.DroneStatus.MOVING:
                if report.destination == report.position:
                    command = commands.Command.create_halt_command()
                    print("Drone is moving")

        # if at waypoint
        else:
            print("accessed here", status)
            if status == drone_status.DroneStatus.HALTED:
                print("access here too", self.padx, self.pady)
                dx = self.padx - position.location_x
                dy = self.pady - position.location_y
                print("accessed here 3")
                if dx <= self.acceptance_radius and dy <= self.acceptance_radius:
                    command = commands.Command.create_land_command()
                    print("Landing at pad...")
                elif self.padx <= 60 and self.pady <= 60:
                    command = commands.Command.create_set_relative_destination_command(dx, dy)
            elif status == drone_status.DroneStatus.MOVING:
                if report.destination == report.position:
                    command = commands.Command.create_halt_command()
                    print("Drone done moving")
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
