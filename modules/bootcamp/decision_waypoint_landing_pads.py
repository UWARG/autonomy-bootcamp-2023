"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


import math
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

        self.plan = ["waypoint", "landing_pad"]

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

        # Do something based on the report and the state of this class...
        def euclidean_dist(p1: location.Location, p2: location.Location):
            return math.sqrt((p1.location_x - p2.location_x)**2 + (p1.location_y - p2.location_y)**2)
        
        # account for cases where target exceeds flight boundary        
        def controlled_destination(p1: location.Location, p2: location.Location):
            x = p1.location_x - p2.location_x
            y = p1.location_y - p2.location_y

            if (abs(x) > 60 or abs(y) > 60):
                magnitude = euclidean_dist(p1, p2)
                x = x / magnitude * 60
                y = y / magnitude * 60
                print(x, y)

            return x, y

        if (report.status == drone_status.DroneStatus.HALTED):
            if (euclidean_dist(report.position, self.waypoint) > self.acceptance_radius or len(self.plan) >= 1):
                action = self.plan.pop(0)

                if (action == "landing_pad"):
                    self.waypoint = min(landing_pad_locations, key=lambda location : euclidean_dist(location, report.position))

                x, y = controlled_destination(self.waypoint, report.position)
                command = commands.Command.create_set_relative_destination_command(x, y)
            else:
                command = commands.Command.create_land_command()

        elif (report.status == drone_status.DroneStatus.MOVING):
            if (euclidean_dist(report.position, self.waypoint) > self.acceptance_radius):
                command = commands.Command.create_null_command()
            else:
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
