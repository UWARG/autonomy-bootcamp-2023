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
        self.at_waypoint = False
        self.bestpad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def calc_dis_squared(self, position: location.Location, pad: location.Location) -> float:
        dist_x = abs(pad.location_x - position.location_x)
        dist_y = abs(pad.location_y - position.location_y)
        return dist_x ** 2 + dist_y ** 2

    def find_pad(self,
                report: drone_report.DroneReport,
                landing_pad_locations: "list[location.Location]") -> commands.Command: 
        # find which one is closest
        if len(landing_pad_locations) > 0:
            self.bestpad = landing_pad_locations[0]
            bestpad_dist_total_squared = self.calc_dis_squared(report.position, self.bestpad)
        
            for pad in landing_pad_locations:
                dist_total_squared = self.calc_dis_squared(report.position, pad)
                if bestpad_dist_total_squared > dist_total_squared:
                    self.bestpad = pad
                    bestpad_dist_total_squared = dist_total_squared
        else:
            self.bestpad = report.position
     
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
            squared_distance = 0
            if self.at_waypoint:
                relative_x = self.bestpad.location_x - report.position.location_x
                relative_y = self.bestpad.location_y - report.position.location_y
                squared_distance = self.calc_dis_squared(report.position, self.bestpad)
            else:
                relative_x = self.waypoint.location_x - report.position.location_x
                relative_y = self.waypoint.location_y - report.position.location_y
                squared_distance = self.calc_dis_squared(report.position, self.waypoint)
            
            if squared_distance > self.acceptance_radius ** 2:
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

            if self.at_waypoint and squared_distance <= self.acceptance_radius ** 2:
                command = commands.Command.create_land_command()
            elif not self.at_waypoint and squared_distance <= self.acceptance_radius ** 2:
                # find which one is closest
                self.find_pad(report, landing_pad_locations)
                self.at_waypoint = True
                
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
