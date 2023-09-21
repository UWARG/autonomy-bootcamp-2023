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

        self.has_taken_off = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def is_same(self, postition: location.Location, destination: location.Location) -> bool:
        """
        To determine if postion of the drone is within the acceptable radius of its destination.
        """
        # check in x direction
        if abs(destination.location_x - postition.location_x) > self.acceptance_radius:
             return False

        # check in y direction
        if abs(destination.location_y - postition.location_y) > self.acceptance_radius:
             return False

        return True
        
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

        # Do something based on the report and the state of this class...\
       
        # actions for once drone has reached destination
        if self.is_same(report.position, report.destination) and self.has_taken_off:
            if report.status == drone_status.DroneStatus.MOVING:  # halt if previously moving
                command = commands.Command.create_halt_command()
            if report.status == drone_status.DroneStatus.HALTED:  # land if previously halted
                command = commands.Command.create_land_command()


        # set destination to waypoint before drone takes off, and set take off status
        # to allow setting destination to waypoint before checking 
        if not self.has_taken_off:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y  - report.position.location_y)
                self.has_taken_off = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
