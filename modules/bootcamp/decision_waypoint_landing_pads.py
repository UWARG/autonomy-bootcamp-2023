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

        # State tracking
        self.reached_waypoint = False
        self.selected_landing_pad = None
        self.movement_attempted = False
        self.last_position = None
        self.stationary_count = 0

    def _calculate_distance(self, pos1: location.Location, pos2: location.Location) -> float:
        """
        Calculate the Euclidean distance between two locations.
        """
        return (
            (pos1.location_x - pos2.location_x) ** 2 + (pos1.location_y - pos2.location_y) ** 2
        ) ** 0.5

    def _find_nearest_landing_pad(
        self, current_pos: location.Location, landing_pads: "list[location.Location]"
    ) -> location.Location:
        """
        Find the nearest landing pad using squared distance.
        """
        if not landing_pads:
            return None

        nearest_pad = landing_pads[0]
        min_squared_dist = self._calculate_distance(current_pos, nearest_pad) ** 0.5

        for pad in landing_pads[1:]:
            squared_dist = self._calculate_distance(current_pos, pad) ** 0.5
            if squared_dist < min_squared_dist:
                min_squared_dist = squared_dist
                nearest_pad = pad

        return nearest_pad

    def _is_stationary(self, current_pos: location.Location) -> bool:
        """
        Check if drone hasn't moved significantly since last update.
        """
        if self.last_position is None:
            self.last_position = current_pos
            return True

        is_stationary = self._calculate_distance(current_pos, self.last_position) < 0.001
        self.last_position = current_pos
        return is_stationary

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

        distance_to_waypoint = self._calculate_distance(report.position, self.waypoint)

        # Check if we're stationary
        if self._is_stationary(report.position):
            self.stationary_count += 1
        else:
            self.stationary_count = 0

        # If we've reached the waypoint, select landing pad if not already selected
        if distance_to_waypoint <= self.acceptance_radius and not self.selected_landing_pad:
            self.reached_waypoint = True
            self.selected_landing_pad = self._find_nearest_landing_pad(
                report.position, landing_pad_locations
            )

        # If we have a selected landing pad, navigate to it
        if self.selected_landing_pad:
            distance_to_pad = self._calculate_distance(report.position, self.selected_landing_pad)

            # If we're close enough to the pad, land
            if distance_to_pad <= self.acceptance_radius:
                if report.status == drone_status.DroneStatus.HALTED:
                    return commands.Command.create_land_command()

                return commands.Command.create_halt_command()

            # If halted, move toward pad
            if report.status == drone_status.DroneStatus.HALTED:
                dx = self.selected_landing_pad.location_x - report.position.location_x
                dy = self.selected_landing_pad.location_y - report.position.location_y

                # Verify movement stays within boundaries
                target_x = report.position.location_x + dx
                target_y = report.position.location_y + dy

                if abs(target_x) <= 60.0 and abs(target_y) <= 60.0:
                    return commands.Command.create_set_relative_destination_command(dx, dy)

        # If we haven't reached waypoint yet, navigate to it
        elif report.status == drone_status.DroneStatus.HALTED:
            dx = self.waypoint.location_x - report.position.location_x
            dy = self.waypoint.location_y - report.position.location_y

            # Verify movement stays within boundaries
            target_x = report.position.location_x + dx
            target_y = report.position.location_y + dy

            if abs(target_x) <= 60.0 and abs(target_y) <= 60.0:
                self.movement_attempted = True
                return commands.Command.create_set_relative_destination_command(dx, dy)

        # If we're stuck or outside boundaries, halt
        if self.stationary_count > 5:
            return commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
