"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.has_sent_landing_command = False
        self.commenced_landing_procedure = False
        self.pad_location = location.Location(0.0, 0.0)
        self.pad_location_x = 0.0
        self.pad_location_y = 0.0

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def clearance(self, position: location.Location) -> bool:
        """Function checks whether the drone has reached waypoint without using square root operation"""
        distance_x = self.waypoint.location_x - position.location_x
        distance_y = self.waypoint.location_y - position.location_y
        distance_squared = distance_x**2 + distance_y**2
        clear = distance_squared < self.acceptance_radius**2
        return clear

    def findpad(
        self,
        current_location: "location.Location",
        landing_pad_locations: "list[location.Location]",
    ) -> location.Location:
        """
        Find the closest landing pad and return its location
        """
        closest_index = 0
        smallest_distance_squared = float("inf")
        for i, curr in enumerate(landing_pad_locations):
            distance_x = curr.location_x - current_location.location_x
            distance_y = curr.location_y - current_location.location_y
            distance_squared = distance_x**2 + distance_y**2
            if distance_squared < smallest_distance_squared:
                closest_index = i
                smallest_distance_squared = distance_squared
        return landing_pad_locations[closest_index]

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
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

        if report.status == drone_status.DroneStatus.HALTED:
            # If the drone is halted, then get it to the proper stage of action
            if not self.clearance(report.position) and not self.commenced_landing_procedure:
                # In this case, the drone need to head to the waypoint
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y,
                )
            elif self.clearance(report.position):
                # The drone need to head to the landing pad
                # If no landing pad spotted, land directly
                if len(landing_pad_locations) == 0:
                    command = commands.Command.create_land_command()
                closest_landing_pad = self.findpad(report.position, landing_pad_locations)
                self.pad_location.location_x = closest_landing_pad.location_x
                self.pad_location.location_y = closest_landing_pad.location_y
                command = commands.Command.create_set_relative_destination_command(
                    self.pad_location.location_x - report.position.location_x,
                    self.pad_location.location_y - report.position.location_y,
                )
                # Indicate that the drone is heading to landing pad
                self.commenced_landing_procedure = True
            elif not self.has_sent_landing_command:
                # In this case, the drone need to land
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True
        elif report.status == drone_status.DroneStatus.MOVING:
            if self.clearance(report.position) and not self.commenced_landing_procedure:
                # stop the drone if it reaches the waypoint
                command = commands.Command.create_halt_command()
            elif self.clearance(self.pad_location):
                # stop the drone if it reaches the waypoint
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
