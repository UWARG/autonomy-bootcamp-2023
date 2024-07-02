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

        self.waypoint_status = False
        self.acceptance_radius_sq = self.acceptance_radius ** 2
        
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

        if self.waypoint_status:  # if at waypoint
            command = self.handle_waypoint_reached(report, landing_pad_locations)
        else:  # go to waypoint
            command = self.handle_waypoint_not_reached(report)
        
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def handle_waypoint_reached(self, report, landing_pad_locations):
        command = commands.Command.create_null_command()
        if report.status == drone_status.DroneStatus.HALTED:
            if self.nearest_landing_pad is None:
                self.nearest_landing_pad = self.find_nearest_landing_pad(report.position, landing_pad_locations)
            if self.relative_dist_sq(report.position, self.nearest_landing_pad) > self.acceptance_radius_sq:
                command = commands.Command.create_set_relative_destination_command(
                    self.nearest_landing_pad.location_x - report.position.location_x,
                    self.nearest_landing_pad.location_y - report.position.location_y,
                )
            else:
                command = commands.Command.create_land_command()
        elif report.status == drone_status.DroneStatus.MOVING:
            if self.relative_dist_sq(report.position, self.nearest_landing_pad) < self.acceptance_radius_sq:
                command = commands.Command.create_halt_command()
        return command

    def handle_waypoint_not_reached(self, report):
        command = commands.Command.create_null_command()

        if self.relative_dist_sq(report.position, self.waypoint) < self.acceptance_radius_sq:
            self.waypoint_status = True

        if report.status == drone_status.DroneStatus.HALTED:
            if not self.waypoint_status:  # Only create command if waypoint is not reached
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
        elif report.status == drone_status.DroneStatus.MOVING:
            if self.relative_dist_sq(report.position, self.waypoint) < self.acceptance_radius_sq:
                command = commands.Command.create_halt_command()
                self.waypoint_status = True
                
        return command

    def relative_dist_sq(self, position: location.Location, destination: location.Location) -> float:
        return (position.location_x - destination.location_x) ** 2 + (position.location_y - destination.location_y) ** 2

    def find_nearest_landing_pad(self, position: location.Location, landing_pad_locations: "list[location.Location]") -> location.Location:
        nearest_landing_pad = None
        nearest_distance = float("inf")
        for landing_pad in landing_pad_locations:
            distance = self.relative_dist_sq(position, landing_pad)
            if distance < nearest_distance:
                nearest_landing_pad = landing_pad
                nearest_distance = distance
        return nearest_landing_pad
