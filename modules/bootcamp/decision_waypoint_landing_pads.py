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

        # Class variable to store landing pad location
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

        # Do something based on the report and the state of this class...
        
        # When drone is HALTED and the drone is not at the waypoint then move towards waypoint
        if report.status == drone_status.DroneStatus.HALTED and report.position != self.waypoint:
            waypoint_relative_to_drone_x = self.waypoint.location_x - report.position.location_x
            waypoint_relative_to_drone_y = self.waypoint.location_y - report.position.location_y

            command = commands.Command.create_set_relative_destination_command(
                waypoint_relative_to_drone_x,
                waypoint_relative_to_drone_y,
            )

        # When drone is HALTED and the drone is at the desired waypoint then find closest landing pad
        # and move towards selected landing pad location 
        if report.status == drone_status.DroneStatus.HALTED and report.position == self.waypoint:
            landing_pad_distances = []
            for i in range(0, len(landing_pad_locations)):
                distance = self.distance_to_landing_pad(landing_pad_locations[i], report.position)
                landing_pad_distances.append(distance)

            shortest_distance = landing_pad_distances[0]
            closest_landing_pad_index = 0

            for i in range(1, len(landing_pad_distances)):
                if landing_pad_distances[i] < shortest_distance:
                    shortest_distance = landing_pad_distances[i]
                    closest_landing_pad_index = i

            closest_landing_pad_location = landing_pad_locations[closest_landing_pad_index]

            closest_pad_relative_to_drone_x = closest_landing_pad_location.location_x - report.position.location_x
            closest_pad_relative_to_drone_y = closest_landing_pad_location.location_y - report.position.location_y

            command = commands.Command.create_set_relative_destination_command(
                closest_pad_relative_to_drone_x,
                closest_pad_relative_to_drone_y,
            )

            self.landing_pad = closest_landing_pad_location

        # When drone is HALTED and the drone is at the desired landing pad then land
        if self.landing_pad is not None and report.position == self.landing_pad:
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def distance_to_landing_pad(self,
                                landing_pad_location: location.Location,
                                drone_location: location.Location) -> float:
        pad_relative_to_drone_x = landing_pad_location.location_x - drone_location.location_x
        pad_relative_to_drone_y = landing_pad_location.location_y - drone_location.location_y

        distance = math.sqrt(pad_relative_to_drone_x ** 2 + pad_relative_to_drone_y ** 2)

        return distance
