"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.at_waypoint = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def dist_to_pad_squared(self, pad: location.Location):
        relative_x = pad.location_x - self.waypoint.location_x
        relative_y = pad.location_y - self.waypoint.location_y
        return relative_x ** 2 + relative_y ** 2

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
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

        if report.status == drone_status.DroneStatus.HALTED:
            relative_x = self.waypoint.location_x - report.position.location_x
            relative_y = self.waypoint.location_y - report.position.location_y
            if relative_x ** 2 + relative_y ** 2 < self.acceptance_radius ** 2 and not self.at_waypoint:
                self.at_waypoint = True
            elif not self.at_waypoint:
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
            else:
                min_pad_dist = float('inf')
                closest = None
                for pad in landing_pad_locations:
                    pad_dist = self.dist_to_pad_squared(pad)
                    if pad_dist < min_pad_dist:
                        min_pad_dist = pad_dist
                        closest = pad
                if closest is not None:
                    relative_x = closest.location_x - report.position.location_x
                    relative_y = closest.location_y - report.position.location_y
                if relative_x ** 2 + relative_y ** 2 <= self.acceptance_radius ** 2:
                    command = commands.Command.create_land_command()
                    self.landing_requested = True
                else: 
                    command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
