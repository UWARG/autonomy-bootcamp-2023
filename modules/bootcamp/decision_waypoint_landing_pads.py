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
    navigate to the waypoint and land at the nearest available pad.
    """

    def __init__(self, waypoint: location.Location, radius: float) -> None:
        self.waypoint = waypoint
        print(f"waypoint at: {waypoint}")
        self.radius = radius
        self.arrived = False
        self.closest_pad = None

    def distance_squared(self, a: location.Location, b: location.Location) -> float:
        dx = a.location_x - b.location_x
        dy = a.location_y - b.location_y
        return dx * dx + dy * dy

    def find_closest_pad(self, pos: location.Location, pads: "list[location.Location]") -> None:
        min_dist = float("inf")
        for pad in pads:
            dist = self.distance_squared(pos, pad)
            if dist < min_dist:
                min_dist = dist
                self.closest_pad = pad

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
        command = commands.Command.create_null_command()

        stat = report.status
        pos_now = report.position

        if self.arrived:
            if stat == drone_status.DroneStatus.HALTED:
                if self.distance_squared(pos_now, self.closest_pad) < self.radius**2:
                    command = commands.Command.create_land_command
                    print("halted, landing initiated")
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.closest_pad.location_x - pos_now.location_x,
                        self.closest_pad.location_y - pos_now.location_y,
                    )
                    print("navigating to landing pad")
            elif stat == drone_status.DroneStatus.MOVING:
                if self.distance_squared(pos_now, self.closest_pad) < self.radius**2:
                    command = commands.Command.create_halt_command()
                    print("halting")
        else:
            if stat == drone_status.DroneStatus.HALTED:
                if self.distance_squared(pos_now, self.waypoint) < self.radius**2:
                    self.find_closest_pad(pos_now, landing_pad_locations)
                    self.arrived = True
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - pos_now.location_x,
                        self.waypoint.location_y - pos_now.location_y,
                    )
                    print("heading to waypoint")
            elif (
                stat == drone_status.DroneStatus.MOVING
                and self.distance_squared(pos_now, self.waypoint) < self.radius**2
            ):
                command = commands.Command.create_halt_command()

        return command
