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

        self._phase = "WAYPOINT"
        self._closest_pad = None

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

        if report.status == drone_status.DroneStatus.LANDED:
            return command

        def dist_sq(loc1: location.Location, loc2: location.Location) -> float:
            dx = loc1.x - loc2.x
            dy = loc1.y - loc2.y
            return dx * dx + dy * dy

        if self._phase == "WAYPOINT":
            if (
                dist_sq(report.position, self.waypoint)
                <= self.acceptance_radius * self.acceptance_radius
            ):
                if report.status == drone_status.DroneStatus.HALTED:
                    closest_dist_sq = float("inf")
                    chosen_pad = None
                    for pad in landing_pad_locations:
                        pad_dist_sq = dist_sq(self.waypoint, pad)
                        if pad_dist_sq < closest_dist_sq:
                            closest_dist_sq = pad_dist_sq
                            chosen_pad = pad
                    if chosen_pad is None:
                        return commands.Command.create_land_command()
                    self._closest_pad = chosen_pad
                    self._phase = "PAD"
                    return command
                return command
            if report.status == drone_status.DroneStatus.HALTED:
                dx = self.waypoint.x - report.position.x
                dy = self.waypoint.y - report.position.y
                return commands.Command.create_set_relative_destination_command(dx, dy)
            return command

        if self._phase == "PAD":
            if self._closest_pad is not None:
                if (
                    dist_sq(report.position, self._closest_pad)
                    <= self.acceptance_radius * self.acceptance_radius
                ):
                    if report.status == drone_status.DroneStatus.HALTED:
                        return commands.Command.create_land_command()
                    return command
                if report.status == drone_status.DroneStatus.HALTED:
                    dx = self._closest_pad.x - report.position.x
                    dy = self._closest_pad.y - report.position.y
                    return commands.Command.create_set_relative_destination_command(dx, dy)
                return command

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
