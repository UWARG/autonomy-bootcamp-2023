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
        self.goal = commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y) # top right?
        self.finished_goal = False
        self.should_land = False
        # BC NOTE: From Task #3

        self.closest_landing_pad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
    def create_close_pad_goal(self, reference_location : location.Location, landing_pad_locations : list[location.Location]) -> commands.Command:
        """
        Calculates and sets self.closest_landing_pad based on a given reference location
        """
        # assuming landing_pad_locations is always populated, but just in-case
        if not landing_pad_locations:
            return commands.Command.create_null_command()
        sorted_locations = landing_pad_locations.copy()
        sorted_locations.sort(
            key=lambda location: ((location.location_x - reference_location.location_x) ** 2 + (location.location_y - reference_location.location_y) ** 2
        )) 
        closest_pad : location.Location = sorted_locations[0]
        rel_x = closest_pad.location_x - reference_location.location_x
        rel_y = closest_pad.location_y - reference_location.location_y
        return commands.Command.create_set_relative_destination_command(rel_x, rel_y)

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

        # Do something based on the report and the state of this class...

        # only execute when "drone" is ready for another instruction
        if report.status == drone_status.DroneStatus.HALTED:
            if self.should_land:
                command = commands.Command.create_land_command()
            elif self.finished_goal:
                command = self.create_close_pad_goal(report.position, landing_pad_locations)
                self.should_land = True # should land on the next instruction
            else:
                command = self.goal
                self.finished_goal = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
