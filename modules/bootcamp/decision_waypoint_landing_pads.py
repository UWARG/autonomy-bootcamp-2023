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

        self.reached = False
        self.best_pad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def dis_squared (self, drone, pad):
        """
        Calculate the distance between the drone's current position and the waypoint
        """
        return ((pad.location_x - drone.location_x) ** 2 + 
                (pad.location_y - drone.location_y) ** 2)
    
    def find_best_pad (self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        find the closest pad
        """
        if len(landing_pad_locations) > 0:
            self.best_pad = landing_pad_locations[0]
            bestpad_dist_squared = self.dis_squared(report.position, landing_pad_locations[0])

            for current_pad in landing_pad_locations:
                current_dist_squared = self.dis_squared(report.position, current_pad)
                if current_dist_squared < bestpad_dist_squared:
                    self.best_pad = current_pad
                    bestpad_dist_squared = current_dist_squared
        
        else:
            self.best_pad = None


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
        rel_x = self.waypoint.location_x - report.position.location_x
        rel_y = self.waypoint.location_y - report.position.location_y

        if report.status == drone_status.DroneStatus.HALTED:
            if self.reached:
                rel_x = self.best_pad.location_x - report.position.location_x
                rel_y = self.best_pad.location_y - report.position.location_y

            command = commands.Command.create_set_relative_destination_command(rel_x, rel_y)

            if self.reached and (rel_x ** 2 + rel_y ** 2) <= self.acceptance_radius ** 2:
                command = commands.Command.create_land_command()
            
            if not self.reached and (rel_x ** 2 + rel_y ** 2) <= self.acceptance_radius ** 2:
                self.find_best_pad(report, landing_pad_locations) # find nearest landing pad
                self.reached = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
