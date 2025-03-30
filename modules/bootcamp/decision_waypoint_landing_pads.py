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
        self._phase = 0
        self._has_set_destination = False
        self._has_landed = False
        self._landing_pad_location = None

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
        status = report.status
        current_pos = report.position

        if status == drone_status.DroneStatus.LANDED:
            return command

        if self._phase == 0:
            distance_to_waypoint = self._distance(current_pos, self.waypoint)
            if distance_to_waypoint <= self.acceptance_radius**2:
                self._phase = 1
                self._has_set_destination = False
            else:
                command = self._move_toward(report, self.waypoint)
                self._has_set_destination = True
        elif self._phase == 1:
            if self._landing_pad_location is None:
                if landing_pad_locations:
                    self._landing_pad_location = self._find_closest_landing_pad(
                        current_pos, landing_pad_locations
                    )
                else:
                    self._landing_pad_location = self.waypoint
            distance_to_pad = self._distance(current_pos, self._landing_pad_location)
            if distance_to_pad <= self.acceptance_radius**2:
                self._phase = 2
                self._has_set_destination = False
            else:
                command = self._move_toward(report, self._landing_pad_location)
                self._has_set_destination = True
        elif self._phase == 2:
            distance_to_pad = self._distance(current_pos, self._landing_pad_location)
            if distance_to_pad > self.acceptance_radius**2:
                self._phase = 1
            else:
                if status == drone_status.DroneStatus.HALTED and not self._has_landed:
                    command = commands.Command.create_land_command()
                    self._has_landed = True
                elif status != drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_halt_command()

        return command

    def _distance(self, loc1: location.Location, loc2: location.Location) -> float:
        dy = loc2.location_y - loc1.location_y
        dx = loc2.location_x - loc1.location_x
        return dx**2 + dy**2

    def _find_closest_landing_pad(
        self, current_pos: location.Location, pads: "list[location.Location]"
    ) -> location.Location:
        closest_pad = None
        min_dist = float("inf")
        for pad in pads:
            dist = self._distance(current_pos, pad)
            if dist < min_dist:
                min_dist = dist
                closest_pad = pad
        return closest_pad

    def _move_toward(
        self, report: drone_report.DroneReport, target: location.Location
    ) -> commands.Command:
        if self._has_set_destination:
            return commands.Command.create_null_command()
        if report.status == drone_status.DroneStatus.HALTED:
            dx = target.location_x - report.position.location_x
            dy = target.location_y - report.position.location_y
            self._has_set_destination = True
            return commands.Command.create_set_relative_destination_command(dx, dy)
        return commands.Command.create_null_command()
