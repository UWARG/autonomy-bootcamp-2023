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
        self.min_bounds = -60
        self.max_bounds = 60

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def min_dist_squared(self, landing_pads: location.Location) -> float:
        """returns distance squared"""
        dist = (self.waypoint.location_x - landing_pads.location_x) ** 2 + (
            self.waypoint.location_y - landing_pads.location_y
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
            proximity = (self.waypoint.location_x - report.position.location_x) ** 2 + (
                self.waypoint.location_y - report.position.location_y
            ) ** 2
            new_pad = location.Location(0, 0)
            # checking if the drone is halted
            if report.status == drone_status.DroneStatus.HALTED:

                #when drone is at the nearest landing pad
                if self.has_sent_landing_command:
                    command = commands.Command.create_land_command()

                #finding nearest landing pad anf setting relative destination
                elif not self.has_sent_landing_command and proximity < self.acceptance_radius**2:
                    smallest_dist = float("inf")
                    for landing_pads in landing_pad_locations:
                        new_dist = self.min_dist_squared(landing_pads)
                        if new_dist < smallest_dist:
                            smallest_dist = new_dist
                            new_pad = landing_pads

                    command = commands.Command.create_set_relative_destination_command(
                        new_pad.location_x - self.waypoint.location_x,
                        new_pad.location_y - self.waypoint.location_y,
                    )
                    self.has_sent_landing_command = True

                #setting relative destination to waypoint
                elif proximity > self.acceptance_radius and not self.has_sent_landing_command:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x, self.waypoint.location_y
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
