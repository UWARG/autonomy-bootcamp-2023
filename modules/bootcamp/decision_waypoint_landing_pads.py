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
import math

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
        self.step = 0
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

        #Step 1: Travel to waypoint
        if (self.step == 0):
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
            self.step = 1
        elif (self.step == 1 and report.status.value == 1):
            self.closest_pad = landing_pad_locations[0]
            # for i in range (landing_pad_locations):
            if (getDist(landing_pad_locations[0].location_x, landing_pad_locations[0].location_y, report.position.location_x, report.position.location_y) < getDist(self.closest_pad.location_x, self.closest_pad.location_y, report.position.location_x, report.position.location_y)):
                self.closest_pad = landing_pad_locations[0]
            command = commands.Command.create_set_relative_destination_command(self.closest_pad.location_x - report.position.location_x, self.closest_pad.location_y - report.position.location_y)
            print("Moving")
            self.step = 2
        elif (self.step == 2 and report.status.value == 1):
            print("Activate")
            command = commands.Command.create_land_command()


        # Remove this when done
       #raise NotImplementedError

        

        
        
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command


def getDist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) 