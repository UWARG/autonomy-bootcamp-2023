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

        # Add your own
        self.created_waypoint_command = False
        self.selected_landing_pad = None
        self.has_sent_landing_command = False

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

        if report.status == drone_status.DroneStatus.HALTED and not self.created_waypoint_command:
            print("Reached waypoint: " + str(report.position))
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
            self.created_waypoint_command = True

        elif report.status == drone_status.DroneStatus.HALTED and self.selected_landing_pad is None:

            print("selecting closest landing pad")
            # select a landing pad that's closest to current position
            min_distance = float('inf')
            for landing_pad in landing_pad_locations:
                print("Checking distance for: ", landing_pad)
                distance = math.sqrt((landing_pad.location_x - report.position.location_x)**2 + (landing_pad.location_y - report.position.location_y)**2)
                if distance < min_distance:
                    min_distance = distance
                    self.selected_landing_pad = landing_pad
            # add a new command
            command = commands.Command.create_set_relative_destination_command(
                self.selected_landing_pad.location_x - report.position.location_x,
                self.selected_landing_pad.location_y - report.position.location_y
            )
            print("Selected landing pad: " + str(self.selected_landing_pad))

        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command and self.selected_landing_pad is not None:
            print("Landing at: " + str(report.position))
            # is landing the drone
            command = commands.Command.create_land_command()

            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
