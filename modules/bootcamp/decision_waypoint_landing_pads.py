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

        self.land = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def _distance_between_locations(self, l1: location.Location, l2: location.Location) -> float:
        """
        Returns the distance between two locations, used by the within_radius function
        """
        x1 = l1.location_x
        x2 = l2.location_x
        y1 = l1.location_y
        y2 = l2.location_y
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance

    def _squared_distance_between_locations(
        self, l1: location.Location, l2: location.Location
    ) -> float:
        x1 = l1.location_x
        x2 = l2.location_x
        y1 = l1.location_y
        y2 = l2.location_y
        distance = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance

    def _within_radius(self, current_location: location.Location) -> bool:
        """
        Returns whether the drone is within the waypoint
        """
        distance = self._distance_between_locations(current_location, self.waypoint)
        print(distance, self.acceptance_radius)
        if distance < self.acceptance_radius:
            return True
        return False

    def _find_landing_pad(
        self, current_location: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> location.Location:
        closest_landing_pad = landing_pad_locations[0]
        for i in landing_pad_locations[1:]:
            closest_distance = self._squared_distance_between_locations(
                current_location, closest_landing_pad
            )
            new_distance = self._squared_distance_between_locations(current_location, i)
            if closest_distance > new_distance:
                closest_landing_pad = i

        return closest_landing_pad

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

        current_position = report.position
        current_status = report.status
        current_destination = report.destination
        # moving = 0
        # halted = 1
        # landed = 2

        if current_status.value == 1 and self._within_radius(
            current_position
        ):  # the drone is at the waypoint and stopped
            closest_landing_pad = self._find_landing_pad(current_position, landing_pad_locations)
            self.waypoint = closest_landing_pad
            if self.land:
                command = commands.Command.create_land_command()
            else:
                self.land = True
        elif (
            current_status.value == 0 and self.waypoint == current_position
        ):  # necessary? Halt when reach the waypoint
            command = commands.Command.create_halt_command()

        elif current_destination != self.waypoint or (
            current_status.value == 1 and not self._within_radius(current_position)
        ):  # incorrect final destination or halt location
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - current_position.location_x,
                self.waypoint.location_y - current_position.location_y,
            )

        elif (
            current_status.value == 0 and current_destination == self.waypoint
        ) or current_status.value == 2:  # drone is travelling towards waypoint or already landed
            command = commands.Command.create_null_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
