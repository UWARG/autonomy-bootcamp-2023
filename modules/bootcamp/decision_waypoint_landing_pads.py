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

        self.reached_waypoint = False
        self.nearest_landing_pad = None

    def squared_distance(self, loc_1: location.Location, loc_2: location.Location) -> float:
        """
        Calculates the squared distances of two locations
        """

        x_distance = loc_1.location_x - loc_2.location_x
        y_distance = loc_1.location_y - loc_2.location_y
        return (x_distance**2) + (y_distance**2)

    def set_nearest_landing_pads(
        self, position: location.Location, landing_pads: "list[location.Location]"
    ) -> None:
        """
        Sets the nearest landing pad
        """
        nearest_distance = float("inf")
        for landing_pad in landing_pads:
            landing_pad_distance = self.squared_distance(position, landing_pad)
            if landing_pad_distance < nearest_distance:
                nearest_distance = landing_pad_distance
                self.nearest_landing_pad = landing_pad

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

        status = report.status
        waypoint_position = self.waypoint
        current_position = report.position

        # If we are at the waypoint
        if self.reached_waypoint:
            if status == drone_status.DroneStatus.HALTED:
                if (
                    self.squared_distance(current_position, self.nearest_landing_pad)
                    < self.acceptance_radius**2
                ):
                    command = commands.Command.create_land_command
                    print("Halted, heading to landing pad")
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.nearest_landing_pad.location_x - current_position.location_x,
                        self.nearest_landing_pad.location_y - current_position.location_y,
                    )
                    print("Heading to landing pad")
            elif status == drone_status.DroneStatus.MOVING:
                if (
                    self.squared_distance(current_position, self.nearest_landing_pad)
                    < self.acceptance_radius ** 2
                ):
                    command = commands.Command.create_halt_command()
                    print("Halting")
        # Else if we are heading to waypoiont
        else:
            if status == drone_status.DroneStatus.HALTED:
                if (
                    self.squared_distance(current_position, waypoint_position)
                    < self.acceptance_radius ** 2
                ):
                    self.set_nearest_landing_pads(current_position, landing_pad_locations)
                    self.reached_waypoint = True
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        waypoint_position.location_x - current_position.location_x,
                        waypoint_position.location_y - current_position.location_y,
                    )
                    print("Heading to waypoint")
            elif (
                status == drone_status.DroneStatus.MOVING
                and self.squared_distance(current_position, waypoint_position)
                < self.acceptance_radius ** 2
            ):
                command = commands.Command.create_halt_command()

        return command
