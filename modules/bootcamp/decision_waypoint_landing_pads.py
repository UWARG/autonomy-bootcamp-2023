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

        self.at_start = True
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


        required_dist_x = self.waypoint.location_x - report.position.location_x
        required_dist_y = self.waypoint.location_y - report.position.location_y


        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:
            if  abs(required_dist_x) < 0.1 and abs(required_dist_y) < 0.1:
                if self.at_start == False: # if not at start, then ok to land
                    command = commands.Command.create_land_command()
            else:
                self.at_start = False
                command = commands.Command.create_set_relative_destination_command(required_dist_x, required_dist_y)

        if report.status == drone_status.DroneStatus.MOVING and abs(required_dist_x) < 0.1 and abs(required_dist_y) < 0.1:
            command = commands.Command.create_halt_command()
        # Remove this when done
        #raise NotImplementedError

        min_dist = 10000 #max possible dist is 60^2 + 60^2, so anything > 7200 works for an initial value
        closest_landing_pad = self.waypoint

        for landing_pad_location in landing_pad_locations:
            #distance can be calculated by sqrt((x1-x2)^2 - (y1-y2)^2), so order is preserved if we do (x1-x2)^2 - (y1-y2)^2 (and saves computation time w/o using sqrt)
            if (landing_pad_location.location_x - report.position.location_x) ** 2 - (landing_pad_location.location_y - report.position.location_y) ** 2 < min_dist:
                min_dist = (landing_pad_location.location_x - report.position.location_x) ** 2 - (landing_pad_location.location_y - report.position.location_y) ** 2
                closest_landing_pad = landing_pad_location
        self.waypoint = closest_landing_pad

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
