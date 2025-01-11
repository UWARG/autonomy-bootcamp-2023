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

        self.above_destination = False
        self.target_lp = None

        self.approaching_wp = False
        self.approaching_lp = False

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
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # print("RUN")
        # Default command
        command = commands.Command.create_null_command()

        if report.status == drone_status.DroneStatus.HALTED:
            print("HALTED AT:   ", report.position.location_x, report.position.location_y)
            print(
                "DESTINATION WAS:   ", report.destination.location_x, report.destination.location_y
            )

            # Handle unexpected halts
            delta_x = report.position.location_x - report.destination.location_x
            delta_y = report.position.location_y - report.destination.location_y
            self.above_destination = delta_x**2 + delta_y**2 < self.acceptance_radius**2

            if not self.above_destination:
                print("^^UNEXPECTED HALT")
                command = commands.Command.create_set_relative_destination_command(
                    report.destination.location_x - report.position.location_x,
                    report.destination.location_y - report.position.location_y,
                )

            elif not self.approaching_wp:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x, self.waypoint.location_y
                )
                self.approaching_wp = True
                print("APPROACHING WP:  ", self.waypoint.location_x, self.waypoint.location_y)

            elif not self.approaching_lp:
                self.target_lp = self.find_closest_lp(report, landing_pad_locations)
                lp_relative_x, lp_relative_y = self.relative_target(self.target_lp, report)

                command = commands.Command.create_set_relative_destination_command(
                    lp_relative_x, lp_relative_y
                )
                self.approaching_lp = True
                print("APPROACHING LP:  ", self.target_lp.location_x, self.target_lp.location_y)

            else:
                command = commands.Command.create_land_command()
                print("LANDING")

        return command

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def find_closest_lp(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> int:
        """
        Given a list of landing pads,
        determines the index of the closest one to the waypoint.
        """
        if len(landing_pad_locations) == 1:
            return landing_pad_locations[0]

        drone_x = report.position.location_x
        drone_y = report.position.location_y

        i = 0
        winning_pad = landing_pad_locations[0]
        winning_sq_dist = float("inf")

        for lp in landing_pad_locations:
            lp_x = lp.location_x
            lp_y = lp.location_y

            delta_x = lp_x - drone_x
            delta_y = lp_y - drone_y

            sq_dist = delta_x**2 + delta_y**2

            if sq_dist < winning_sq_dist:
                winning_sq_dist = sq_dist
                winning_pad = landing_pad_locations[i]

            i += 1

        # print("TARGET LP FOUND, INDEX: ", winning_i)
        # print("^^SQDIST FROM WP:  ", winning_dist)
        return winning_pad

    @staticmethod
    def relative_target(
        target: location.Location, report: drone_report.DroneReport
    ) -> tuple[int, int]:
        """
        Returns the x and y of a target relative to the drone's current position
        """

        diff_x = target.location_x - report.position.location_x
        diff_y = target.location_y - report.position.location_y

        # print("RELATIVE TARGET: ", diff_x, diff_y)
        return diff_x, diff_y
