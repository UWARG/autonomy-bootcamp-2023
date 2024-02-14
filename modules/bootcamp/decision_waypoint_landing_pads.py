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
        self.close = 0
        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        self.visited = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
    def distance_calculator(self, startx, starty, finalx, finaly):
        return ((finalx-startx)**2 + (finaly-starty)**2)**(1/2)

    def find_min(self, l, startx, starty):
        mins = self.distance_calculator(startx, starty, l[0].location_x, l[0].location_y)
        i = l[0]
        l.pop(0)
        for pad in l:
            dis = self.distance_calculator(startx, starty, pad.location_x, pad.location_y)
            if dis < mins:
                mins = dis
                i = pad
        return i
    
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
        pos = report.position
        w_x = self.waypoint.location_x
        w_y = self.waypoint.location_y
        r = self.acceptance_radius
        halted = drone_status.DroneStatus.HALTED
        move = commands.Command.create_set_relative_destination_command
        if self.visited == True and report.status == halted and (self.close.location_x - pos.location_x)**2 + (self.close.location_y - pos.location_y)**2 < r**2:
            command = commands.Command.create_land_command()
        elif report.status == halted and (w_x - pos.location_x)**2 + (w_y - pos.location_y)**2 <= r**2:
            self.visited = True
            self.close = self.find_min(landing_pad_locations, pos.location_x, pos.location_y)
            command = move(self.close.location_x - pos.location_x, self.close.location_y - pos.location_y)
        elif report.status == halted and self.visited == False:
            command = move(w_x - pos.location_x, w_y - pos.location_y)
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
