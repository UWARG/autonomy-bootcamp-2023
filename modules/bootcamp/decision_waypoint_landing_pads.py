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
        self.reached_waypoint = False

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

        x_delta = 0
        y_delta = 0
        dist = 10000

        if self.reached_waypoint is False:
            x_delta = self.waypoint.location_x - report.position.location_x
            y_delta = self.waypoint.location_y - report.position.location_y
            dist = (x_delta * x_delta + y_delta * y_delta) ** 0.5

        if self.reached_waypoint is True:
            print("waypoint reached")
            x_delta_set = landing_pad_locations[0].location_x - report.position.location_x
            y_delta_set = landing_pad_locations[0].location_y - report.position.location_y
            dist = (x_delta_set * x_delta_set + y_delta_set * y_delta_set) ** 0.5

            for landing_pad in landing_pad_locations:
                x_delta_landing = landing_pad.location_x - report.position.location_x
                y_delta_landing = landing_pad.location_y - report.position.location_y

                if (
                    x_delta_landing * x_delta_landing + y_delta_landing * y_delta_landing
                ) <= dist**2:
                    x_delta_set = x_delta_landing
                    y_delta_set = y_delta_landing
                    dist = (x_delta_set * x_delta_set + y_delta_set * y_delta_set) ** 0.5

            x_delta = x_delta_set
            y_delta = y_delta_set

        if dist <= self.acceptance_radius and self.reached_waypoint is True:
            command = commands.Command.create_land_command()
            return command

        if dist <= self.acceptance_radius and self.reached_waypoint is False:
            self.reached_waypoint = True

        if report.status == drone_status.DroneStatus.HALTED and dist > self.acceptance_radius:
            # we are currently stopped so check the next closest waypoint to our destination
            if (x_delta > 60 or x_delta < -60) or (y_delta > 60 or y_delta < -60):
                command = commands.Command.create_null_command()
                return command
            command = commands.Command.create_set_relative_destination_command(x_delta, y_delta)
        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
