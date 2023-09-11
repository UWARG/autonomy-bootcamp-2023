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

        self.timeline = "initial"

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

        # print(landing_pad_locations)

        x1, y1 = report.position.location_x, report.position.location_y

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:
            if self.timeline == "initial":
                x2, y2 = self.waypoint.location_x, self.waypoint.location_y
                relative_x = x2 - x1
                relative_y = y2 - y1
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

                self.timeline = "initial-moving"
            elif self.timeline == "initial-moving":
                closest_x, closest_y = landing_pad_locations[0].location_x, landing_pad_locations[0].location_y
                closest_dist = math.dist([x1, y1], [closest_x, closest_y])

                for i in range(1, len(landing_pad_locations)):
                    new_x, new_y = landing_pad_locations[i].location_x, landing_pad_locations[i].location_y
                    new_dist = math.dist([x1, y1], [new_x, new_y])

                    if new_dist < closest_dist:
                        closest_dist = new_dist
                        closest_x = new_x
                        closest_y = new_y

                relative_x = closest_x - x1
                relative_y = closest_y - y1
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

                self.timeline = "waypoint-moving"
                self.landing_x = closest_x
                self.landing_y = closest_y
            else:
                command = commands.Command.create_land_command()

                self.timeline = "landed"


        elif report.status == drone_status.DroneStatus.MOVING:
            if self.timeline == "initial-moving":
                x2, y2 = self.waypoint.location_x, self.waypoint.location_y
                dist = math.dist([x1, y1], [x2, y2])

                if dist <= self.acceptance_radius:
                    command = commands.Command.create_halt_command()

            else:
                x2, y2 = self.landing_x, self.landing_y
                dist = math.dist([x1, y1], [x2, y2])

                if dist <= self.acceptance_radius:
                    command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
