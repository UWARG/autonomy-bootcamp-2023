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

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Square acceptance radius to compare relative distance
        self.acceptance_radius_squared = acceptance_radius**2
        self.drone_status = 1

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

        drone_halted = (report.status == drone_status.DroneStatus.HALTED)
        if self.drone_status == 1:
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)
            self.drone_status = 2
        elif drone_halted and self.drone_status == 2:
            if dist(report.position.location_x, report.position.location_y, self.waypoint.location_x, self.waypoint.location_y <= self.acceptance_radius_squared):
                self.target = locate_landing_pad(report.position, landing_pad_locations)
                command = commands.Command.create_set_relative_destination_command(self.target.location_x - report.position.location_x, self.target.location_y - report.position.location_y) 
                self.drone_status = 3
            else:
                self.drone_status = 1
        elif drone_halted and self.drone_status == 3:
            if dist(report.position.location_x, report.position.location_y, self.target.location_x, self.target.location_y) <= self.acceptance_radius_squared:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(self.target.location_x - report.position.location_x, self.target.location_y - report.position.location_y)
        
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

def locate_landing_pad(position, landing_pad_locations):
        # Start with a very large number
        min_dist = float("inf")
        target = None
        for location in landing_pad_locations:
            x = dist(location.location_x, location.location_y, position.location_x, position.location_y)
            if x < min_dist:
                min_dist = x
                target = location
        return target

def dist(x_coor_1, y_coor_1, x_coor_2, y_coor_2):
    """ Calculates the Euclidean distance between two points without using the square root function"""
    return (x_coor_2 - x_coor_1)**2 + (y_coor_2 - y_coor_1)**2
