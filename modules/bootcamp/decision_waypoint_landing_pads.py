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

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.waypoint_found = False
        self.landing_pad_found = False
        self.go_to_waypoint = commands.Command.create_set_relative_destination_command(
            waypoint.location_x,
            waypoint.location_y,
        )

        self.landed = False

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

        if report.status == drone_status.DroneStatus.HALTED and not self.waypoint_found:
            print("Halted at: " + str(report.position))
            self.waypoint_found = True
            command = self.go_to_waypoint
        elif report.status == drone_status.DroneStatus.HALTED and not self.landing_pad_found:
            print("Halted at: " + str(report.position))
            self.landing_pad_found = True
            min_distance_squared = float('inf')
            closest_pad = None
            for landing_pad in landing_pad_locations:
                distance_squared = (landing_pad.location_x - report.position.location_x) ** 2 \
                                 + (landing_pad.location_y - report.position.location_y) ** 2
                if distance_squared < min_distance_squared:
                    min_distance_squared = distance_squared
                    closest_pad = landing_pad
            command = commands.Command.create_set_relative_destination_command(
                closest_pad.location_x - report.position.location_x,
                closest_pad.location_y - report.position.location_y,
            )
            self.landing_pad_found = True
        elif report.status == drone_status.DroneStatus.HALTED and self.landing_pad_found:
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
