"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use


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

        self.reached_waypoint = False
        self.target_landing_pad = location.Location(9999, 9999)

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

        def distance_squared(point_1: location.Location, point_2: location.Location) -> float:
            return (point_1.location_x - point_2.location_x) ** 2 + (
                point_1.location_y - point_2.location_y
            ) ** 2

        def reached_target(current_position: location.Location, target: location.Location) -> bool:
            return bool(distance_squared(current_position, target) <= self.acceptance_radius**2)

        def set_relative_direction(
            point_1: location.Location, point_2: location.Location
        ) -> commands.Command:
            relative_x = point_2.location_x - point_1.location_x
            relative_y = point_2.location_y - point_1.location_y
            return commands.Command.create_set_relative_destination_command(relative_x, relative_y)

        if (
            reached_target(report.position, self.waypoint)
            and report.status == drone_status.DroneStatus.MOVING
            and not self.reached_waypoint
        ):
            # reaching waypoint
            command = commands.Command.create_halt_command()
            self.reached_waypoint = True
            distances_to_pads: list[float] = []
            for pad_location in landing_pad_locations:
                distances_to_pads.append(distance_squared(pad_location, self.waypoint))
            min_distance = min(distances_to_pads)
            min_index = distances_to_pads.index(min_distance)
            self.target_landing_pad = landing_pad_locations[min_index]
        elif not reached_target(report.position, self.waypoint) and not self.reached_waypoint:
            # before reaching waypoint
            command = set_relative_direction(report.position, self.waypoint)
        elif (
            reached_target(report.position, self.target_landing_pad)
            and report.status == drone_status.DroneStatus.MOVING
        ):
            # reaching landing pad and HALTing
            command = commands.Command.create_halt_command()
        elif (
            reached_target(report.position, self.target_landing_pad)
            and report.status == drone_status.DroneStatus.HALTED
        ):
            # landing on the pad
            command = commands.Command.create_land_command()
        else:
            # after reaching waypoint but before reaching landing pad
            command = set_relative_direction(report.position, self.target_landing_pad)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
