"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
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
class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        self.looking_for_waypoint: bool = True

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
        def __distance_squared(pos: location.Location, dest: location.Location) -> float:
            return (pos.location_x - dest.location_x)**2 + (pos.location_y - dest.location_y)**2

        def __find_closest_landing_pad() -> location.Location:
            min_distance: float = 30000
            closest_landing_pad: location.Location = None
            for landing_pad_location in landing_pad_locations:
                dist: float = __distance_squared(
                    landing_pad_location, report.position)
                if dist < min_distance:
                    min_distance = dist
                    closest_landing_pad = landing_pad_location
            return closest_landing_pad

        if report.status == drone_status.DroneStatus.HALTED:
            if self.looking_for_waypoint:
                dy: float = self.waypoint.location_y - report.position.location_y
                dx: float = self.waypoint.location_x - report.position.location_x
            else:
                landing_pad: location.Location = __find_closest_landing_pad()
                dy: float = landing_pad.location_y - report.position.location_y
                dx: float = landing_pad.location_x - report.position.location_x

            if abs(dy) > self.acceptance_radius and abs(dx) > self.acceptance_radius:
                command = commands.Command.create_set_relative_destination_command(
                    dx, dy)
            elif self.looking_for_waypoint:
                self.looking_for_waypoint = False
                command = commands.Command.create_halt_command()
            else:
                command = commands.Command.create_land_command()

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
