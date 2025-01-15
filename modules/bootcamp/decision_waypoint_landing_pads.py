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

        # Add your own
        self.target = None
        self.tol = 0.0001

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
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

        if not self.target and report.status == drone_status.DroneStatus.HALTED:
            self.target = self.find_closest_landing_pad(report.position, landing_pad_locations)

        # If the drone is halted and not at the destination, move the drone to destination
        if report.status == drone_status.DroneStatus.HALTED and report.destination != self.target:

            command = commands.Command.create_set_relative_destination_command(
                self.target.location_x, self.target.location_y
            )
        # if the drone is at the destination and halted land the drone
        elif report.status == drone_status.DroneStatus.HALTED and report.destination == self.target:
            command = commands.Command.create_land_command()

        # Case handling to ensure that the drone tries to land again if it lands outside of the acceptance radius
        if (
            report.status == drone_status.DroneStatus.LANDED
            and (report.position - report.destination) > self.acceptance_radius
        ):
            command = commands.Command.create_set_relative_destination_command(
                self.target.location_x, self.target.location_y
            )

        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    @staticmethod
    def find_closest_landing_pad(
        current_location: location.Location, destination_list: "list[location.Location]"
    ) -> location.Location:
        """
        Takes the current location and a list of possible destinations and calculates the
        closest destination. This location.Location object is returned.

        Args:
            current_location (location.Location): Location the drone is currently at (0, 0)
            destination_list (list[location.Location]): list of possible destinations for the drone

        Returns:
            location.Location: class implementation of a location defined by x and y
        """
        if len(destination_list) > 0:
            destination = location.Location(float('inf'), float('inf'))
            for landing_pad in destination_list:
                landing_pad_distance = (landing_pad.location_x - current_location.location_x) ** 2 + (landing_pad.location_y - current_location.location_y) ** 2
                destination_distance = (destination.location_x - current_location.location_x) ** 2 + (destination.location_y - current_location.location_y) ** 2
                if landing_pad_distance < destination_distance:
                    destination = landing_pad
        else:
            destination = location.Location(0, 0)
        return destination

        
