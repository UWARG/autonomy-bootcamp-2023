"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use


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
        self.has_sent_landing_command = False
        self.send_landing_command = False
        self.reached_landing_pad = False
        self.min_bounds = -60
        self.max_bounds = 60

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def distance_to_pad_squared(
        self, report: drone_report.DroneReport, landing_pad: location.Location
    ) -> float:
        """returns distance squared"""
        dist = (report.position.location_x - landing_pad.location_x) ** 2 + (
            report.position.location_y - landing_pad.location_y
        ) ** 2
        return dist

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
        if (
            self.waypoint.location_x >= self.min_bounds
            and self.waypoint.location_x <= self.max_bounds
            and self.waypoint.location_y >= self.min_bounds
            and self.waypoint.location_y <= self.max_bounds
        ):

            if report.status == drone_status.DroneStatus.HALTED:

                if self.send_landing_command:
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
                    return command

                # calculating location of nearest landing pad
                smallest_dist_x = float("inf")
                smallest_dist_y = float("inf")
                smallest_dist = smallest_dist_x**2 + smallest_dist_y**2
                for landing_pad in landing_pad_locations:
                    new_dist = self.distance_to_pad_squared(report, landing_pad)
                    if new_dist < smallest_dist:
                        smallest_dist = new_dist
                        smallest_dist_x = landing_pad.location_x
                        smallest_dist_y = landing_pad.location_y

                # if drone is at the waypoint
                if (
                    (self.waypoint.location_x - report.position.location_x) ** 2
                    + (self.waypoint.location_y - report.position.location_y) ** 2
                ) < self.acceptance_radius**2:

                    # if nearest landing pad is at the waypoint, land
                    if smallest_dist < self.acceptance_radius**2:
                        self.send_landing_command = True

                    # if not, set relative destination to nearest landing pad
                    else:
                        command = commands.Command.create_set_relative_destination_command(
                            smallest_dist_x - report.position.location_x,
                            smallest_dist_y - report.position.location_y,
                        )
                        self.reached_landing_pad = True

                # drone moves to nearest landing pad, then lands
                elif self.reached_landing_pad:
                    self.send_landing_command = True

                # if drone halts unexpectedly, neither at the waypoint or at the nearest landing pad
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y,
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
