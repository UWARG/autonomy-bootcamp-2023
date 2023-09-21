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

    @staticmethod
    def get_distance(location_a: location.Location, location_b: location.Location) -> float:
        """
        Get the distance between two locations.
        """
        return ((location_a.location_x-location_b.location_x)**2 + (location_a.location_y-location_b.location_y)**2)**0.5

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
        if report.status == drone_status.DroneStatus.MOVING:
            if DecisionSimpleWaypoint.get_distance(report.position,self.waypoint) < self.acceptance_radius:
                command = commands.Command.create_halt_command()
        elif report.status == drone_status.DroneStatus.HALTED:
            if DecisionSimpleWaypoint.get_distance(report.position,self.waypoint) < self.acceptance_radius:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x-report.position.location_x, self.waypoint.location_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
