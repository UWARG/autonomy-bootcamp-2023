"""
Module to manage drone navigation to a waypoint and landing at the nearest landing pad.

This module provides the DecisionWaypointLandingPads class which is responsible for
directing a drone to a specified waypoint and then finding and landing at the nearest
landing pad, based on the drone's current position and the list of available landing pads.
"""

from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designated waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.

        Args:
            waypoint (location.Location): The waypoint location to travel to.
            acceptance_radius (float): The radius within which the waypoint is considered reached.
        """
        self.waypoint = waypoint
        self.acceptance_radius = acceptance_radius

        # Group related attributes into a single dictionary to reduce attribute count
        self.state = {"waypoint_found": False, "landing_pad_found": False, "closest_pad": None}

    def distance_squared(self, l1: location.Location, l2: location.Location) -> float:
        """
        Calculate the square of the distance between two locations.

        Args:
            l1 (location.Location): The first location.
            l2 (location.Location): The second location.

        Returns:
            float: The square of the distance between the two locations.
        """
        return (l1.location_x - l2.location_x) ** 2 + (l1.location_y - l2.location_y) ** 2

    def is_within_acceptance_radius(self, pos1: location.Location, pos2: location.Location) -> bool:
        """
        Determine if two locations are within the acceptance radius.

        Args:
            pos1 (location.Location): The first location with attributes `location_x` and `location_y`.
            pos2 (location.Location): The second location with attributes `location_x` and `location_y`.

        Returns:
            bool: True if the distance between the two locations is within the acceptance radius.
        """
        return self.distance_squared(pos1, pos2) <= self.acceptance_radius**2

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        Args:
            report (drone_report.DroneReport): Current status report of the drone.
            landing_pad_locations (list[location.Location]): List of available landing pad locations.

        Returns:
            commands.Command: The command for the drone to execute.
        """
        # Default command
        command = commands.Command.create_null_command()

        if report.status != drone_status.DroneStatus.HALTED:
            return command

        # Check if the waypoint is reached
        if not self.state["waypoint_found"]:
            if self.is_within_acceptance_radius(report.position, self.waypoint):
                self.state["waypoint_found"] = True
                print(f"Reached waypoint at {self.waypoint.location_x}, {self.waypoint.location_y}")
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
                print(
                    f"Moving to waypoint at {self.waypoint.location_x}, {self.waypoint.location_y}"
                )
            return command

        # Check if the nearest landing pad is found
        if not self.state["landing_pad_found"]:
            if self.state["closest_pad"] is None:
                self.state["closest_pad"] = min(
                    landing_pad_locations,
                    key=lambda pad: self.distance_squared(report.position, pad),
                )
            if self.is_within_acceptance_radius(report.position, self.state["closest_pad"]):
                self.state["landing_pad_found"] = True
                print(
                    f"Reached landing pad at {self.state['closest_pad'].location_x}, {self.state['closest_pad'].location_y}"
                )
            else:
                command = commands.Command.create_set_relative_destination_command(
                    self.state["closest_pad"].location_x - report.position.location_x,
                    self.state["closest_pad"].location_y - report.position.location_y,
                )
                print(
                    f"Moving to landing pad at {self.state['closest_pad'].location_x}, {self.state['closest_pad'].location_y}"
                )
            return command

        # Land the drone
        if self.state["landing_pad_found"]:
            command = commands.Command.create_land_command()
            print("Landing the drone.")

        return command
