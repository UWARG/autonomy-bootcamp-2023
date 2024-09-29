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

        self.command_index = 0
        self.commands = []
        self.has_sent_landing_command = False
        self.has_reached_waypoint = False
        self.closest_location = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def set_directions(
        self,
        report: drone_report.DroneReport,
        destination: location.Location,
    ) -> None:
        """ "
        set_directions and append it to the list
        """
        x_direction = destination.location_x - report.position.location_x
        y_direction = destination.location_y - report.position.location_y

        self.commands.append(
            commands.Command.create_set_relative_destination_command(x_direction, y_direction)
        )

    def closest_pad(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
    ) -> int | None:
        """ "
        Finds the index of the closest pad
        """
        _min = float("inf")
        closest_index = 0
        index = 0

        for loc in landing_pad_locations:
            x_distance = loc.location_x - report.position.location_x
            y_distance = loc.location_y - report.position.location_y
            if x_distance**2 + y_distance**2 < _min:
                closest_index = index
                _min = x_distance**2 + y_distance**2
            index += 1

        if _min <= self.acceptance_radius**2:
            return None
        return closest_index

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
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

        if len(self.commands) == 0 and not self.has_reached_waypoint:  # set directions
            self.set_directions(report, self.waypoint)

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(
            self.commands
        ):  # execute the command list

            print(self.command_index)
            print(report.status)

            command = self.commands[self.command_index]
            self.command_index += 1

        elif (
            report.status == drone_status.DroneStatus.HALTED and not self.has_reached_waypoint
        ):  # if halted somewhere on the way to the waypoint
            if (
                (report.position.location_x - self.waypoint.location_x) ** 2
                + (report.position.location_y - self.waypoint.location_y) ** 2
            ) <= self.acceptance_radius**2:  # if arrive to the waypoint
                print("It arrived")
                self.has_reached_waypoint = True
            else:
                self.set_directions(report, self.waypoint)
                command = self.commands[self.command_index]
                self.command_index += 1

        if (
            report.status == drone_status.DroneStatus.HALTED
            and self.has_reached_waypoint
            and not self.has_sent_landing_command
        ):  # if halted somewhere on the way to the pad
            if self.closest_location is None:
                closest_index = self.closest_pad(report, landing_pad_locations)
                if closest_index is None:  # if waypoint is directly on the pad simply land
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
                else:
                    self.closest_location = landing_pad_locations[closest_index]
            else:
                if (
                    (report.position.location_x - self.closest_location.location_x) ** 2
                    + (report.position.location_y - self.closest_location.location_y) ** 2
                ) > self.acceptance_radius**2:
                    self.set_directions(report, self.closest_location)
                    command = self.commands[self.command_index]
                    self.command_index += 1
                else:  # if arrive to the landing pad
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        # 1727624842397454200 seed
        return command
