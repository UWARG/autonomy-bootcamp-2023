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

        self.reached_waypoint = False

    @staticmethod
    def distance_sqr(position: location.Location, destination: location.Location) -> float:
        pos_x = position.location_x
        pos_y = position.location_y
        des_x = destination.location_x
        des_y = destination.location_y

        return ((pos_x - des_x) ** 2 + (pos_y - des_y) ** 2)

    @staticmethod
    def in_radius(position: location.Location, destination: location.Location, radius: float) -> bool:
        distance = DecisionWaypointLandingPads.distance_sqr(position, destination)

        return distance < radius ** 2
    
    @staticmethod
    def closest_landing_pad(landing_pad_locations: "list[location.Location]", waypoint: location.Location) -> location.Location:

        closest_lp = None
        min_distance = float("inf")

        for lp in landing_pad_locations:
            distance = DecisionWaypointLandingPads.distance_sqr(lp, waypoint)
            if distance < min_distance:
                min_distance = distance
                closest_lp = lp
        return closest_lp
    
    @staticmethod
    def get_relative(position: location.Location, destination: location.Location) -> "tuple[float,float]":
        dx = destination.location_x - position.location_x
        dy = destination.location_y - position.location_y
        return dx,dy

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

        waypoint = self.waypoint
        position = report.position
        radius = self.acceptance_radius

        if self.reached_waypoint == False:
            if(self.in_radius(position,waypoint,radius)):
                self.reached_waypoint = True
                command = commands.Command.create_halt_command()
                
            else:
                relative_dis = self.get_relative(position,waypoint)
                dx = relative_dis[0]
                dy = relative_dis[1]
                command = commands.Command.create_set_relative_destination_command(dx, dy)

        else:
            closest_lp = self.closest_landing_pad(landing_pad_locations,waypoint)
            if(self.in_radius(position,closest_lp,radius)):
                if(report.status == drone_status.DroneStatus.HALTED):
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_halt_command()
            else:
                relative_dis = self.get_relative(position,closest_lp)
                dx = relative_dis[0]
                dy = relative_dis[1]
                command = commands.Command.create_set_relative_destination_command(dx, dy)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
