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
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        if report.status == drone_status.DroneStatus.HALTED:
            print(f"HALTED AT: ({report.position.location_x}, {report.position.location_y})")
            print(
                f"DESTINATION WAS: ({report.destination.location_x}, {report.destination.location_y})"
            )

            # Handle unexpected halts
            delta_x = report.destination.location_x - report.position.location_x
            delta_y = report.destination.location_y - report.position.location_y
            self.above_destination = delta_x**2 + delta_y**2 < self.acceptance_radius**2

            if not self.above_destination:
                print("^^UNEXPECTED HALT")
                command = commands.Command.create_set_relative_destination_command(delta_x, delta_y)

            # Go to waypoint
            elif not self.approaching_wp:
                waypoint_delta_x = self.waypoint.location_x - report.position.location_x
                waypoint_delta_y = self.waypoint.location_y - report.position.location_y

                command = commands.Command.create_set_relative_destination_command(
                    waypoint_delta_x, waypoint_delta_y
                )
                self.approaching_wp = True
                print("APPROACHING WP:  ", self.waypoint.location_x, self.waypoint.location_y)

            # Find and go to nearest landing pad
            elif not self.approaching_lp:
                self.target_lp = self.find_closest_lp(report, landing_pad_locations)

                if self.target_lp:
                    lp_delta_x = self.target_lp.location_x - report.position.location_x
                    lp_delta_y = self.target_lp.location_y - report.position.location_y

                    command = commands.Command.create_set_relative_destination_command(
                        lp_delta_x, lp_delta_y
                    )
                    self.approaching_lp = True
                    print("APPROACHING LP:  ", self.target_lp.location_x, self.target_lp.location_y)

                # Give a null command if there are no landing pads in landing_pad_locations
                else:
                    command = commands.Command.create_null_command()

            # Landing
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
        # If there's only one pad, default to that one
        if len(landing_pad_locations) == 1:
            return landing_pad_locations[0]

        i = 0
        winning_pad = None
        winning_sq_dist = float("inf")

        for lp in landing_pad_locations:
            delta_x = report.position.location_x - lp.location_x
            delta_y = report.position.location_y - lp.location_y

            sq_dist = delta_x**2 + delta_y**2

            if sq_dist < winning_sq_dist:
                winning_sq_dist = sq_dist
                winning_pad = landing_pad_locations[i]

            i += 1

        return winning_pad
