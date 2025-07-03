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

        self.waypoint = waypoint
        self.acceptance_radius = acceptance_radius
        self.sent_to_waypoint = False
        self.sent_to_pad = False
        self.landed = False
        self.closest_pad = None
        print(f"Waypoint: {waypoint}")

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

        current = report.position

        def distance_squared(a: location.Location, b: location.Location) -> float:
            return (a.location_x - b.location_x) ** 2 + (a.location_y - b.location_y) ** 2

        # if landed
        #if report.status == drone_status.DroneStatus.LANDED:
        #    return command

        # If halted
        if report.status == drone_status.DroneStatus.HALTED:
            if not self.sent_to_waypoint:
                dist_to_waypoint_sq = distance_squared(current, self.waypoint)
                if dist_to_waypoint_sq <= self.acceptance_radius ** 2:
                    # reached waypoint
                    min_dist = float("inf")
                    for pad in landing_pad_locations:
                        dist = distance_squared(current, pad)
                        if dist < min_dist:
                            min_dist = dist
                            self.closest_pad = pad
                    self.sent_to_waypoint = True
                else:
                    # Move to waypoint
                    rel_x = self.waypoint.location_x - current.location_x
                    rel_y = self.waypoint.location_y - current.location_y
                    new_x = current.location_x + rel_x
                    new_y = current.location_y + rel_y
                    if -60 <= new_x <= 60 and -60 <= new_y <= 60:
                        command = commands.Command.create_set_relative_destination_command(
                            rel_x, rel_y
                        )

            elif not self.sent_to_pad:
                dist_to_pad_sq = distance_squared(current, self.closest_pad)
                if dist_to_pad_sq <= self.acceptance_radius ** 2:
                    command = commands.Command.create_land_command()
                    self.sent_to_pad = True
                    self.landed = True
                else:
                    rel_x = self.closest_pad.location_x - current.location_x
                    rel_y = self.closest_pad.location_y - current.location_y
                    new_x = current.location_x + rel_x
                    new_y = current.location_y + rel_y
                    if -60 <= new_x <= 60 and -60 <= new_y <= 60:
                        command = commands.Command.create_set_relative_destination_command(
                            rel_x, rel_y
                        )

        # If drone is moving and reached target
        elif report.status == drone_status.DroneStatus.MOVING:
            target = self.closest_pad if self.sent_to_waypoint else self.waypoint
            dist_sq = distance_squared(current, target)
            if dist_sq <= self.acceptance_radius ** 2:
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
