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

        self.target_lp = None

        self.reached_wp = False
        self.reached_lp = False

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
        # print("RUN")
        # Default command
        command = commands.Command.create_null_command()

        if report.status == drone_status.DroneStatus.HALTED:
            print("HALTED AT:   ", report.position.location_x, report.position.location_y)
            print(
                "DESTINATION WAS:   ", report.destination.location_x, report.destination.location_y
            )

            # Handle unexpected halts
            if report.position != report.destination:
                print("^^UNEXPECTED HALT")
                command = commands.Command.create_set_relative_destination_command(
                    report.destination.location_x - report.position.location_x,
                    report.destination.location_y - report.position.location_y,
                )

            elif not self.reached_wp:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x, self.waypoint.location_y
                )
                self.reached_wp = True
                print("APPROACHING WP:  ", self.waypoint.location_x, self.waypoint.location_y)

            elif not self.reached_lp:
                self.target_lp = landing_pad_locations[self.find_closest_lp(landing_pad_locations)]
                lp_relative_x, lp_relative_y = self.relative_target(self.target_lp, report)
                command = commands.Command.create_set_relative_destination_command(
                    lp_relative_x, lp_relative_y
                )
                self.reached_lp = True
                print("APPROACHING LP:  ", self.target_lp.location_x, self.target_lp.location_y)

            else:
                command = commands.Command.create_land_command()
                print("LANDING")

        return command

    def find_closest_lp(self, landing_pad_locations: "list[location.Location]") -> int:
        """
        Given a list of landing pads,
        determines the index of the closest one to the waypoint.
        """
        if len(landing_pad_locations) in [0, 1]:
            return 0

        wp_x = self.waypoint.location_x
        wp_y = self.waypoint.location_y

        i = 0
        winning_i = 0
        winning_dist = -1

        for lp in landing_pad_locations:
            lp_x = lp.location_x
            lp_y = lp.location_y

            same_loc = (
                wp_x - self.acceptance_radius <= lp_x <= wp_x + self.acceptance_radius
            ) and (wp_y - self.acceptance_radius <= lp_y <= wp_y + self.acceptance_radius)

            if same_loc:
                return i

            sq_dist = (lp_x - wp_x) ** 2 + (lp_y - wp_y) ** 2

            if (sq_dist < winning_dist) or (winning_dist == -1):
                winning_dist = sq_dist
                winning_i = i

            i += 1

        # print("TARGET LP FOUND, INDEX: ", winning_i)
        # print("^^SQDIST FROM WP:  ", winning_dist)
        return winning_i

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
