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
import math


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
        self.state = "initiated"

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def __distance(self,
                 location1: location.Location,
                 location2: location.Location) -> float:
        return (location2.location_x-location1.location_x)**2+(location2.location_y-location1.location_y)**2

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
        if report.position.location_x == 0 and report.position.location_y == 0 and report.status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_set_relative_destination_command(float(self.waypoint.location_x), float(self.waypoint.location_y))
        elif report.status == drone_status.DroneStatus.HALTED and report.position == self.waypoint:
            print("reached waypoint")
            closest_pad_distance = 10**378
            closest_pad_index = -1
            for i in range(len(landing_pad_locations)):
                distance = self.__distance(self.waypoint, landing_pad_locations[i])
                if distance < closest_pad_distance:
                    closest_pad_distance = distance
                    closest_pad_index = i
            print(f"closest landing pad: {landing_pad_locations[closest_pad_index]}")
            command = commands.Command.create_set_relative_destination_command((landing_pad_locations[i].location_x-report.position.location_x), (landing_pad_locations[i].location_y - report.position.location_y))
            self.state = "past waypoint"
        elif report.status == drone_status.DroneStatus.HALTED and self.state == "past waypoint":
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
