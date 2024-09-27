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
        self.acceptance_radius_squared = self.acceptance_radius**2  # used for distance calculation
        self.finding_waypoint = True
        self.nearest_landing_pad_location = location.Location(0, 0)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def find_nearest_pad(
        reference_location: location.Location, landing_pad_locations: list[location.Location]
    ) -> location.Location:
        """
        Calculates returns nearest landing pad location based on a given reference location
        """
        # assuming landing_pad_locations is always populated, but just in-case
        closest_location = min(
            landing_pad_locations,
            key=lambda location: (
                (location.location_x - reference_location.location_x) ** 2
                + (location.location_y - reference_location.location_y) ** 2
            ),
            default=location.Location(0, 0),
        )
        return closest_location

    @staticmethod
    def calculate_distance_squared(
        from_location: location.Location, to_location_x: float, to_location_y: float
    ) -> float:
        """
        Calculate the non-square rooted distance between two locations
        """
        return (to_location_x - from_location.location_x) ** 2 + (to_location_y - from_location.location_y) ** 2

    @staticmethod
    def get_relative_position(
        from_location: location.Location, to_location: location.Location
    ) -> tuple[float, float]:
        """
        Calculates the relative position of one position to another
        """
        return (
            to_location.location_x - from_location.location_x,
            to_location.location_y - from_location.location_y,
        )

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

        # only execute when "drone" is ready for another instruction
        if report.status == drone_status.DroneStatus.HALTED:
            if self.finding_waypoint:
                if (
                    DecisionWaypointLandingPads.calculate_distance_squared(
                        report.position, self.waypoint.location_x, self.waypoint.location_y
                    )
                    <= self.acceptance_radius_squared
                ):
                    self.finding_waypoint = False
                    self.nearest_landing_pad_location = (
                        DecisionWaypointLandingPads.find_nearest_pad(
                            report.position, landing_pad_locations
                        )
                    )
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x, self.waypoint.location_y
                    )
            else:
                if (
                    DecisionWaypointLandingPads.calculate_distance_squared(
                        report.position,
                        self.nearest_landing_pad_location.location_x,
                        self.nearest_landing_pad_location.location_y,
                    )
                    <= self.acceptance_radius_squared
                ):
                    command = commands.Command.create_land_command()
                else:
                    relative_x, relative_y = DecisionWaypointLandingPads.get_relative_position(
                        report.position, self.nearest_landing_pad_location
                    )
                    command = commands.Command.create_set_relative_destination_command(
                        relative_x, relative_y
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
