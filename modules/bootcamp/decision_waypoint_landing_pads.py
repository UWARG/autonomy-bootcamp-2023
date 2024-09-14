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

        self.achieved_waypoint = False

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

        if not self.achieved_waypoint:
            dx, dy = self._calc_relative_dist(report.position, self.waypoint)
            if dx**2 + dy**2 > self.acceptance_radius**2:
                if report.status != drone_status.DroneStatus.MOVING:
                    command = commands.Command.create_set_relative_destination_command(dx, dy)
            else:
                self.achieved_waypoint = True
        if self.achieved_waypoint:
            # now we find the index of the landing pad closest to the drone
            # while keeping that landing pad's distance (squared)

            dx, dy = 0, 0
            if len(landing_pad_locations) > 0:
                # in the case that landing_pad_locations is not empty,
                # we try to go to the nearest landing pad
                best_index, shortest_dist = 0, self._calc_distance_squared(
                    report, landing_pad_locations[0]
                )
                for i in range(1, len(landing_pad_locations)):
                    dist = self._calc_distance_squared(report, landing_pad_locations[i])
                    if dist < shortest_dist:
                        best_index, shortest_dist = i, dist

                dx, dy = self._calc_relative_dist(
                    report.position, landing_pad_locations[best_index]
                )
            else:
                # otherwise, we go back to the origin
                dx, dy = -report.position.location_x, -report.position.location_y

            if dx**2 + dy**2 > self.acceptance_radius**2:
                if report.status != drone_status.DroneStatus.MOVING:
                    command = commands.Command.create_set_relative_destination_command(dx, dy)
            elif report.status == drone_status.DroneStatus.MOVING:
                command = commands.Command.create_halt_command()
            elif report.status == drone_status.DroneStatus.HALTED:
                command = commands.Command.create_land_command()
            # otherwise, the drone is already landed at the closest landing pad
            # and we are done because the command is already the null command

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def _calc_distance_squared(
        self, report: drone_report.DroneReport, destination: location.Location
    ) -> int:
        dx, dy = self._calc_relative_dist(report.position, destination)
        return dx**2 + dy**2

    def _calc_relative_dist(
        self, loc1: location.Location, loc2: location.Location
    ) -> "tuple[int, int]":
        """Relative location from loc1 to loc2

        Args:
            loc1 (location.Location): Location 1
            loc2 (location.Location): Location 2

        Returns:
            tuple[int, int]: dx, dy
        """
        return loc2.location_x - loc1.location_x, loc2.location_x - loc1.location_x
