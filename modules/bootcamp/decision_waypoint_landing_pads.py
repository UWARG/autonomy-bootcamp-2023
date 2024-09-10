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
        self.command_index = 0

        self.commands = []

        self.has_sent_landing_command = False
        self.has_found_landing_pad = False

        self.counter = 0

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
        if report.status == drone_status.DroneStatus.HALTED:
            # Defined here so that report object can be used
            self.commands = [
                commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
            ]
            if self.command_index < len(self.commands):
                command = self.commands[self.command_index]
                self.command_index += 1
            elif not self.has_found_landing_pad:
                # uses simple minimum value search to find closest pad and goes there
                dist_min = 30000
                index = 0
                for i in len(landing_pad_locations):
                    dist = (landing_pad_locations[i].location_x - report.position.location_x)**2+(landing_pad_locations[i].location_y - report.position.location_y)**2
                    if dist < dist_min:
                        dist_min = dist
                        index = i

                closest_landing_pad_location = landing_pad_locations[index]

                command = commands.Command.create_set_relative_destination_command(closest_landing_pad_location.location_x - report.position.location_x, closest_landing_pad_location.location_y - report.position.location_y)

                self.has_found_landing_pad = True
            # only runs when on top of landing pad
            else:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
