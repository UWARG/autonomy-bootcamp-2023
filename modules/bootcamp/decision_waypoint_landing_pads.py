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

        distance_away = required_dist_x ** 2 + required_dist_y ** 2

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED:
            if  distance_away < self.acceptance_radius:
                if self.at_start == False: 
                    # if not at start, then drone should be at landing pad
                    # we set landing pad to waypoint below, so won't stop randomly
                    command = commands.Command.create_land_command()
            else:
                # set drone to not be at start anymore
                self.at_start = False
                command = commands.Command.create_set_relative_destination_command(required_dist_x, required_dist_y)



        min_dist = float('inf') #max possible dist is 60^2 + 60^2, so anything > 7200 works for an initial value
        closest_landing_pad = self.waypoint

        if self.at_start == True:
            for landing_pad_location in landing_pad_locations:
                #distance can be calculated by sqrt((x1-x2)^2 - (y1-y2)^2), so order is preserved if we do (x1-x2)^2 - (y1-y2)^2 (and saves computation time w/o using sqrt)
                pad_distance = (landing_pad_location.location_x - report.position.location_x) ** 2 - (landing_pad_location.location_y - report.position.location_y) ** 2
                if pad_distance < min_dist:
                    min_dist = pad_distance
                    closest_landing_pad = landing_pad_location
            # set waypoint to landing pad
            self.waypoint = closest_landing_pad

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
