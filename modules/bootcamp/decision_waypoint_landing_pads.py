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

        self.eps = 0.01
        self.reached_waypoint = False
        self.landing_pad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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
        def sqrdist(p1: location.Location, p2: location.Location):
            dx = p2.location_x - p1.location_x
            dy = p2.location_y - p1.location_y
            return dx * dx + dy * dy

        if self.reached_waypoint:
            if not self.landing_pad:
                self.landing_pad = min(landing_pad_locations, key = lambda pt: sqrdist(pt, self.waypoint))

            if sqrdist(report.position, self.landing_pad) <= self.eps * self.eps:
                if report.status == drone_status.DroneStatus.HALTED:
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_halt_command()
            elif report.status == drone_status.DroneStatus.HALTED:
                dx = self.landing_pad.location_x - report.position.location_x
                dy = self.landing_pad.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(dx, dy)

        elif sqrdist(report.position, self.waypoint) <= self.eps * self.eps:
            command = commands.Command.create_halt_command()
            self.reached_waypoint = True

        elif report.status == drone_status.DroneStatus.HALTED:
            dx = self.waypoint.location_x - report.position.location_x
            dy = self.waypoint.location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(dx, dy)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
