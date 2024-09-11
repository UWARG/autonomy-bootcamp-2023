"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

# Disable for bootcamp use
# pylint: disable=unused-import

import sys
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

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Initialising a boolean variable to check arrival status, and deal with unplanned halts along the way (bonus)
        self.arrived = False

    def squared_distance(self, location1: location.Location, location2: location.Location) -> float:
        """
        Calculate the squared Euclidean distance without square roots
        """
        distance_horizontal = location1.location_x - location2.location_x
        distance_vertical = location1.location_y - location2.location_y
        return distance_horizontal**2 + distance_vertical**2

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def find_closest_landing_pad(
        self,
        current_position: location.Location,
        landing_pad_locations: "list[location.Location]",
    ) -> location.Location:
        """
        Find the closest landing pad
        """
        closest_pad = None
        # Setting default to maximum integer value for easy troubleshooting
        min_distance = sys.maxsize

        # Trivial sorter to determine the closest landing pad
        for lander in landing_pad_locations:
            distance = self.squared_distance(current_position, lander)
            if distance < min_distance:
                min_distance = distance
                closest_pad = lander

        return closest_pad

    def set_destination(
        self, current_position: location.Location, target: location.Location
    ) -> commands.Command:
        """
        Calculates the relative distance and returns a command to move the drone to the target.
        """
        distance_horizontal = target.location_x - current_position.location_x
        distance_vertical = target.location_y - current_position.location_y

        # Setting Destination
        return commands.Command.create_set_relative_destination_command(
            distance_horizontal, distance_vertical
        )

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
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

        # Do something based on the report and the state of this class...

        if not self.arrived:
            current_position = report.position
            squared_distance_to_waypoint = self.squared_distance(current_position, self.waypoint)

            # Check acceptance radius
            if squared_distance_to_waypoint <= self.acceptance_radius**2:
                # Drone arrived!
                self.arrived = True

            else:
                # Dealing with unplanned halts
                if report.status == drone_status.DroneStatus.HALTED:
                    return self.set_destination(report.position, self.waypoint)

        # Repeating process but for closest landing pad, after reaching waypoint
        if self.arrived:
            closest_pad = self.find_closest_landing_pad(report.position, landing_pad_locations)

            # Calculate squared distance to the closest landing pad
            squared_distance_to_pad = self.squared_distance(report.position, closest_pad)

            # If within the acceptance radius of the landing pad, land the drone
            if squared_distance_to_pad <= self.acceptance_radius**2:
                return commands.Command.create_land_command()

            # Move the drone toward the closest landing pad if it's halted
            if report.status == drone_status.DroneStatus.HALTED:
                return self.set_destination(report.position, closest_pad)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
