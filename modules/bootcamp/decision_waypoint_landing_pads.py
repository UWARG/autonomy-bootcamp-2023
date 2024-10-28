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
        self.reached_waypoint = False
        self.border_radius = 60
        self.padx = 0
        self.pady = 0

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def get_nearest_landing(
        self, position: location.Location, landing_pad_locations: "list[location.Location]"
    ) -> None:
        """
        Find the nearest landing pad based on the drone's current position.

        Args:
            position: The current location of the drone.
            landing_pad_locations: A list of available landing pad locations.

        Returns:
            A list of floats containing the x and y coordinates of the nearest landing pad.
        """
        self.padx = landing_pad_locations[0].location_x
        self.pady = landing_pad_locations[0].location_y
        for pad in landing_pad_locations:
            dx = pad.location_x - position.location_x
            dy = pad.location_y - position.location_y
            distance = dx**2 + dy**2
            print(self.padx, self.pady, dx, dy)
            if distance < (
                (self.padx - position.location_x) ** 2 + (self.pady - position.location_y) ** 2
            ):
                self.padx = pad.location_x
                self.pady = pad.location_y

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

        position = report.position
        waypoint = self.waypoint
        status = report.status

        distance_from_waypoint_x = waypoint.location_x - position.location_x
        distance_from_waypoint_y = waypoint.location_y - position.location_y

        if not self.reached_waypoint:
            if status == drone_status.DroneStatus.HALTED:
                if (
                    distance_from_waypoint_x <= self.acceptance_radius
                    and distance_from_waypoint_y <= self.acceptance_radius
                ):
                    self.reached_waypoint = True
                    self.get_nearest_landing(position, landing_pad_locations)
                    print("finding pads...", self.padx, self.pady)
                elif (
                    abs(waypoint.location_x) <= self.border_radius
                    and abs(waypoint.location_y) <= self.border_radius
                ):
                    command = commands.Command.create_set_relative_destination_command(
                        distance_from_waypoint_x, distance_from_waypoint_y
                    )
            elif status == drone_status.DroneStatus.MOVING:
                distance_from_destination = (
                    report.destination.location_x - report.position.location_x
                ) ** 2 + (report.destination.location_y - report.position.location_y) ** 2
                print(distance_from_destination)
                if distance_from_destination <= self.acceptance_radius**2:
                    command = commands.Command.create_halt_command()
                    print("Drone is moving")

        # if at waypoint
        else:
            print("accessed here", status)
            if status == drone_status.DroneStatus.HALTED:
                print("access here too", self.padx, self.pady)
                dx = self.padx - position.location_x
                dy = self.pady - position.location_y
                print("accessed here 3")
                if dx <= self.acceptance_radius and dy <= self.acceptance_radius:
                    command = commands.Command.create_land_command()
                    print("Landing at pad...")
                elif self.padx <= self.border_radius and self.pady <= self.border_radius:
                    command = commands.Command.create_set_relative_destination_command(dx, dy)
            elif status == drone_status.DroneStatus.MOVING:
                distance_from_destination = (
                    report.destination.location_x - report.position.location_x
                ) ** 2 + (report.destination.location_y - report.position.location_y) ** 2
                if distance_from_destination <= self.acceptance_radius**2:
                    command = commands.Command.create_halt_command()
                    print("Drone done moving")
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
