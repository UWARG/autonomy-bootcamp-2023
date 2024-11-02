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

        self.reached_waypoint = False

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

        def get_x_difference(initial: location.Location, final: location.Location):
            return (final.location_x - initial.location_x)
        
        def get_y_difference(initial: location.Location, final: location.Location):
            return (final.location_y - initial.location_y)
        
        def get_distance_squared(diff_x, diff_y):
            return (diff_x*diff_x + diff_y*diff_y)
        
        def get_closest_landing_pad():
            min_distance = 1e20
            closest_landing_pad = None
            for landing_pad in landing_pad_locations:
                x_difference = get_x_difference(report.position, landing_pad)
                y_difference = get_y_difference(report.position, landing_pad)
                if get_distance_squared(x_difference, y_difference) < min_distance:
                    min_distance = get_distance_squared(x_difference, y_difference)
                    closest_landing_pad = landing_pad
            return closest_landing_pad

        if self.reached_waypoint:
            self.waypoint = get_closest_landing_pad()

        x_difference = get_x_difference(report.position, self.waypoint)
        y_difference = get_y_difference(report.position, self.waypoint)
        
        if (get_distance_squared(x_difference,y_difference) >= (self.acceptance_radius*self.acceptance_radius)):
            command = commands.Command.create_set_relative_destination_command(x_difference, y_difference)
        else:
            if not self.reached_waypoint:
                self.reached_waypoint = True
#                command = commands.Command.create_halt_command()
            else:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
