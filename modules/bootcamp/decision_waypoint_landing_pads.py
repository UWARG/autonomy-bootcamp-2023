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

        # Add your own
        self.nearest_landing_pad = None
        self.reached_waypoint = False
        # self.reached_landing_pad = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def _get_distance(self, location1: location.Location, location2: location.Location) -> float:
        """
        Get the distance between two locations.
        """
        return ((location1.location_x - location2.location_x) ** 2 + (location1.location_y - location2.location_y) ** 2) ** 0.5

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

        # If halted, move to the waypoint
        if (report.status == drone_status.DroneStatus.HALTED):

            if (self.nearest_landing_pad is not None) and (self.reached_waypoint) and (self._get_distance(report.position, self.nearest_landing_pad) < self.acceptance_radius):
                command = commands.Command.create_land_command()
            
            # If at the waypoint, halt and search for the nearest landing pad
            elif self._get_distance(report.position, self.waypoint) < self.acceptance_radius:
                if not self.reached_waypoint:
                    self.reached_waypoint = True
                    # Find the nearest landing pad
                    for location in landing_pad_locations:
                        distance = self._get_distance(report.position, location)
                        if (self.nearest_landing_pad is None) or (distance < self._get_distance(report.position, self.nearest_landing_pad)):
                            self.nearest_landing_pad = location

                else:
                    relative_x = self.nearest_landing_pad.location_x - report.position.location_x
                    relative_y = self.nearest_landing_pad.location_y - report.position.location_y
                    command = commands.Command.create_set_relative_destination_command(relative_x=relative_x, relative_y=relative_y)

            else:
                relative_x = self.waypoint.location_x - report.position.location_x
                relative_y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(relative_x=relative_x, relative_y=relative_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
