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

        self.stage = "START"
        self.target = None

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

        def get_ds(p1: location.Location, p2: location.Location) -> float:
            p1x = p1.location_x
            p1y = p1.location_y
            p2x = p2.location_x
            p2y = p2.location_y

            ds = (p1x - p2x) ** 2 + (p1y - p2y) ** 2

            return ds

        def if_reach(des: location.Location, ob: location.Location) -> bool:
            dx = des.location_x
            dy = des.location_y
            ox = ob.location_x
            oy = ob.location_y

            if dx == ox and dy == oy:
                return True
            return False

        if report.status == drone_status.DroneStatus.HALTED and self.stage == "START":
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )
            self.stage = "TOWAYPOINT"

        elif (
            report.status == drone_status.DroneStatus.HALTED
            and self.stage == "TOWAYPOINT"
            and if_reach(self.waypoint, report.position)
        ):
            min_distance = 99999999999999999999999999
            min_landing_pad = None
            for landing_pad in landing_pad_locations:
                distance = get_ds(landing_pad, self.waypoint)
                if distance < min_distance:
                    min_distance = distance
                    min_landing_pad = landing_pad
            self.target = min_landing_pad
            self.stage = "DETECTED"
            print(f"1{report.position}")
            print(f"1{self.target}")

        elif self.stage == "DETECTED":
            print(f"2{report.position}")
            print(f"2{self.target}")
            relative_x = self.target.location_x - report.position.location_x
            relative_y = self.target.location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(
                relative_x, relative_y
            )
            self.stage = "TODESTINATION"

        elif (
            report.status == drone_status.DroneStatus.HALTED
            and if_reach(report.destination, report.position)
            and self.stage == "TODESTINATION"
        ):
            command = commands.Command.create_land_command()
            self.stage = "LANDED"

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
