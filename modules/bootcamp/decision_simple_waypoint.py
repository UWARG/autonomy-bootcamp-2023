"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""
import math

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


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
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

        self.at_waypoint = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

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

        status = report.status


        if self.at_waypoint:
            self.landing_pad = self.get_nearest_landing(report.position, landing_pad_locations)
            complete = self.get_distance(report.position, self.landing_pad) < self.acceptance_radius
            if status == drone_status.DroneStatus.HALTED:
                if(complete):
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_set_relative_destination_command(self.landing_pad.location_x-report.position.location_x,self.landing_pad.location_y-report.position.location_y )
            elif status == drone_status.DroneStatus.MOVING and complete:
                command = commands.Command.create_halt_command()
        else:
            complete = self.get_distance < self.acceptance_radius
            if status == drone_status.DroneStatus.HALTED:
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
                print("Drone is heading to the destination")
            elif status == drone_status.DroneStatus.MOVING and complete:
                command = commands.Command.create_halt_command()
                self.at_waypoint = True


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    def get_nearest_landing(self, position: location.Location, landing_pads: "list[location.Location]") -> location.Location:
        nearest_distance = float("inf")
        nearest_landing_pad = None
        for landing_pad in landing_pads:
            current_distance = self.get_distance(landing_pad, position)
            if current_distance < nearest_distance:
                nearest_distance = current_distance
                nearest_landing_pad = landing_pad
        return nearest_landing_pad

    def get_distance(self, location_1: location.Location, location_2: location.Location):
        "Function returns the distnace of the drone to the target coordinates"
        return math.sqrt(pow(location_1.location_x-location_2.location_x, 2) + pow(location_1.location_y-location_2.location_y, 2))
