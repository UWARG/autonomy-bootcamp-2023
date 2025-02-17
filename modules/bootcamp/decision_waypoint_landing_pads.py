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
        print("Accept radius: ", self.acceptance_radius)

        self.waypoint_complete = False

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

        # add the command to self.commands
        # if halted at waypoint, check if within radius, if so move on, else rerun command
        # if no commands remaining, search for landing pad, new command to move to pad
        # if at landing pad, check if within acceptable radius, if not, redo command, else land

        def within_radius(
            report: drone_report.DroneReport, x: float, y: float, radius: float
        ) -> bool:
            rad2 = radius * radius
            loc = pow(report.position.location_x - x, 2) + pow(report.position.location_y - y, 2)
            if loc > rad2:
                return False
            return True

        def get_distance_squared(report: drone_report.DroneReport, x: float, y: float) -> float:
            return pow(report.position.location_x - x, 2) + pow(report.position.location_y - y, 2)

        def closest_landing(
            report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
        ) -> location.Location:
            closest_dist = float("inf")
            closest_landing_pad = landing_pad_locations[0]
            print("me, x:", report.position.location_x, "y: ", report.position.location_y)
            for landing_pad in landing_pad_locations:
                print("all, x:", landing_pad.location_x, "y:", landing_pad.location_y)
                dist = get_distance_squared(report, landing_pad.location_x, landing_pad.location_y)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_landing_pad = landing_pad
            print(
                "closest, x:", closest_landing_pad.location_x, "y:", closest_landing_pad.location_y
            )
            return closest_landing_pad

        if report.status == drone_status.DroneStatus.HALTED:
            if self.waypoint_complete is False:
                if within_radius(
                    report,
                    self.waypoint.location_x,
                    self.waypoint.location_y,
                    self.acceptance_radius,
                ):
                    self.waypoint_complete = True
                    self.waypoint = closest_landing(report, landing_pad_locations)
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y,
                    )
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y,
                    )
            else:
                if within_radius(
                    report,
                    self.waypoint.location_x,
                    self.waypoint.location_y,
                    self.acceptance_radius,
                ):
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y,
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
