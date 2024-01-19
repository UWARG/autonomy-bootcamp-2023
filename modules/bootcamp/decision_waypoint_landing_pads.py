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

        self.landing_command = False
        self.at_waypoint = False
        self.closest_waypoint = False

    # Helper function: distance between 2 points
    def calculate_distance2(self, p1: location.Location, p2: location.Location) -> float:
        return (p2.location_x - p1.location_x) ** 2 + (p2.location_y - p1.location_y) ** 2

    # Helper function: closest landing pad from the current location
    def closest_lp(self, current_point: location.Location, landing_pad_locations: "list[location.Location]") -> location.Location:
        max_distance = float('inf')
        for landing_pad in landing_pad_locations:
            curr_distance = self.calculate_distance2(current_point, landing_pad)
            
            if curr_distance > max_distance:
                max_distance = curr_distance
                closest_waypoint = landing_pad
        return closest_waypoint 

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

        if report.status == drone_status.DroneStatus.HALTED and not self.at_waypoint: 
            x = self.waypoint.location_x - report.position.location_x
            y = self. waypoint.location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(x, y)
            self.at_waypoint = True
        elif report.status == drone_status.DroneStatus.HALTED and not self.landing_command: 
            command = commands.command.create_land_command()
            self.landing_command = True
        # Identify closest waypoint/landing pad
        elif report.status == drone_status.DroneStatus.HALTED and not self.closest_waypoint:
            closest_lp = self.closest_lp(report.position,landing_pad_locations)
            # Conditional to check for zero landing pads
            if closest_lp is not None:
                command = commands.Command.create_set_relative_destination_command(
                    closest_lp.location_x - report.position.location_x,
                    closest_lp.location_y - report.position.location_y,
                )
                self.closest_waypoint = True
    
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
