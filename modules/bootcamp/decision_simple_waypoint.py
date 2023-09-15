"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""
# Disable for bootcamp use
# pylint: disable=unused-import


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long


# All logic around the run() method
# pylint: disable-next=too-few-public-methods
class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Make the drone fly to the waypoint.

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

        distance_to_waypoint = self.distance_between_points(self.waypoint, report.position)

        if report.status == drone_status.DroneStatus.HALTED and distance_to_waypoint > self.acceptance_radius:
            # When drone is HALTED and the drone is not near the waypoint then move towards waypoint

            # Get relative x and y position of waypoint to drone
            waypoint_relative_to_drone_x = self.waypoint.location_x - report.position.location_x
            waypoint_relative_to_drone_y = self.waypoint.location_y - report.position.location_y

            # Create relative destination command
            command = commands.Command.create_set_relative_destination_command(
                waypoint_relative_to_drone_x,
                waypoint_relative_to_drone_y,
            )

        elif report.status == drone_status.DroneStatus.HALTED and distance_to_waypoint <= self.acceptance_radius:
            # When drone is HALTED and the drone is near the desired waypoint then land

            # Create land command
            command = commands.Command.create_land_command()

        elif report.status == drone_status.DroneStatus.MOVING and distance_to_waypoint <= self.acceptance_radius:
            # When drone is MOVING and the drone is near the desired waypoint then halt

            # Create halt command
            command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    @staticmethod
    def distance_between_points(point_1: location.Location, point_2: location.Location) -> float:
        distance_x = point_1.location_x - point_2.location_x
        distance_y = point_1.location_y - point_2.location_y

        return max(abs(distance_x), abs(distance_y))
