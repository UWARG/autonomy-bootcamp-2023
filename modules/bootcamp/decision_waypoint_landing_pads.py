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
        self.waypoint_reached = False

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

        # Do something based on the report and the state of this class...
        
        # Travel to waypoint
        if report.status == drone_status.DroneStatus.HALTED:
            if not self.waypoint_reached:
                x = self.waypoint.location_x - report.position.location_x
                y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(x, y)
                if (x** 2 + y ** 2) < (self.acceptance_radius ** 2):
                    self.waypoint_reached = True
                    command = commands.Command.create_halt_command()
            else:
                # Find nearest landing pad
                min_dist = float("inf")
                target = None
                for i in landing_pad_locations:
                    dist = (i.location_x - report.position.location_x) ** 2 + (i.location_y - report.position.location_y) ** 2
                    if dist <min_dist:
                        min_dist = dist
                        target = i
                # Travel to nearest landing pad
                x = target.location_x - report.position.location_x
                y = target.location_y - report.position.location_y
                if (x ** 2 + y ** 2) <= (self.acceptance_radius ** 2):
                    # Land
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_set_relative_destination_command(x, y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
