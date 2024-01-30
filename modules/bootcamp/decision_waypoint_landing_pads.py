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
        self.reached_waypoint = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        # Helper Function to Find Distance Between Two Locations
    def distance(self, loc_1: location.Location, loc_2: location.Location):
        loc_1_x = loc_1.location_x
        loc_1_y = loc_1.location_y
        loc_2_x = loc_2.location_x
        loc_2_y = loc_2.location_y
        relative_x_posn = loc_1_x - loc_2_x
        relative_y_posn = loc_1_y - loc_2_y
        return relative_x_posn ** 2 + relative_y_posn ** 2
    
    # Helper Function to Find the Nearest Pad from the Drone's Current Position
    def get_closest_pad(self, curr_posn: location.Location, landing_pads: "list[location.Location]"):
        closest_pad_distance = float("inf")
        closest_pad = None
        for pad in landing_pads:
            if self.distance(pad, curr_posn) < closest_pad_distance:
                closest_pad_distance = self.distance(pad, curr_posn)
                closest_pad = pad
            else:
                pass
        return closest_pad

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
        if report.status == drone_status.DroneStatus.HALTED:
            if not self.reached_waypoint:
                curr_x = report.position.location_x
                curr_y = report.position.location_y
                x_from_curr_posn = self.waypoint.location_x - curr_x
                y_from_curr_posn = self.waypoint.location_y - curr_y
                curr_distance_away = x_from_curr_posn ** 2 + y_from_curr_posn ** 2
                if curr_distance_away > self.acceptance_radius ** 2:
                    command = commands.Command.create_set_relative_destination_command(x_from_curr_posn, y_from_curr_posn)
                else:
                    self.reached_waypoint = True

            else:
                self.waypoint = self.get_closest_pad(report.position, landing_pad_locations)
                curr_x = report.position.location_x
                curr_y = report.position.location_y
                x_from_curr_posn = self.waypoint.location_x - curr_x
                y_from_curr_posn = self.waypoint.location_y - curr_y
                curr_distance_away = x_from_curr_posn ** 2 + y_from_curr_posn ** 2
                if curr_distance_away > self.acceptance_radius ** 2:
                    command = commands.Command.create_set_relative_destination_command(x_from_curr_posn, y_from_curr_posn)
                else:
                    command = commands.Command.create_land_command()

        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command