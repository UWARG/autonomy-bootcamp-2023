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
        self.reaching = True
        self.pad = location.Location
        self.landing = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def get_dist(waypoint: location.Location, pad: location.Location) -> float:
        """
        Calculate distance between waypoint and a landing pad.
        Static method version.
        """
        return (pad.location_x - waypoint.location_x) ** 2 + (
            pad.location_y - waypoint.location_y
        ) ** 2

    @staticmethod
    def reached_destination(
        destination: location.Location, position: location.Location, acceptance_radius: float
    ) -> bool:
        """
        Check if drone is within acceptance radius of target destination.
        Static method version, no access to `self`.
        """
        if (destination.location_x - position.location_x) <= acceptance_radius and (
            destination.location_y - position.location_y
        ) <= acceptance_radius:
            return True
        return False

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:
            if self.reaching:
                reached = self.reached_destination(self.waypoint, report.position, self.acceptance_radius)
                if not reached:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x, self.waypoint.location_y
                    )
                else:
                    mn = float("inf")
                    for i, d in enumerate(landing_pad_locations):
                        d = self.get_dist(self.waypoint, landing_pad_locations[i])
                        if d < mn:
                            mn = d
                            cnt = i
                    self.pad = landing_pad_locations[cnt]
                    command = commands.Command.create_set_relative_destination_command(
                        self.pad.location_x - self.waypoint.location_x,
                        self.pad.location_y - self.waypoint.location_y,
                    )
                    self.reaching = False
            else:
                at_pad = self.reached_destination(self.pad, report.position, self.acceptance_radius)
                if not self.landing and at_pad:
                    command = commands.Command.create_land_command()
                    self.landing = True
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============ 
        return command

