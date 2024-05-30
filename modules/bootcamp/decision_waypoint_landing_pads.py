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

        # Add your own
        self.traveled_to_waypoint = False
        self.has_sent_landing_command = False
        self.closest_landing_pad = None

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
        if report.status == drone_status.DroneStatus.HALTED:
            if not self.traveled_to_waypoint:
                # Fly to the waypoint
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y
                )
                self.traveled_to_waypoint = True
            elif not self.closest_landing_pad:
                # Calculate the closest landing pad
                self.closest_landing_pad = self.find_closest_landing_pad(report.position, landing_pad_locations)
                command = commands.Command.create_set_relative_destination_command(
                    self.closest_landing_pad.location_x - report.position.location_x,
                    self.closest_landing_pad.location_y - report.position.location_y
                )
            elif not self.has_sent_landing_command:
                # Land the drone at the closest landing pad
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True

        # # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    def find_closest_landing_pad(self, current_position: location.Location, landing_pads: "list[location.Location]") -> location.Location:
        """
        Find the closest landing pad to the current position using L-2 norm.
        """
        closest_pad = None
        min_distance = float('inf')

        for pad in landing_pads:
            distance = self.calculate_distance(current_position, pad)
            if distance < min_distance:
                min_distance = distance
                closest_pad = pad

        return closest_pad

    def calculate_distance(self, loc1: location.Location, loc2: location.Location) -> float:
        """
        Calculate the squared distance between two locations to avoid computing square roots.
        """
        return (loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2