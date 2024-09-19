"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        self.landpad_reached = False
        self.waypoint_reached = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
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

            if not self.waypoint_reached:
                # Moves towards the waypoint
                x_dist = self.waypoint.location_x - report.position.location_x
                y_dist = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(x_dist, y_dist)

                self.waypoint_reached = True

            # Once you get to the waypoint, you have to go to the nearest landpad
            elif not self.landpad_reached:
                # Find the closest pad and store it in closest_landpad
                #    This is using the min() method to iterate through each pad, get the distance to it and compare it with others
                closest_pad = min(landing_pad_locations, key=lambda pad: self.get_distance(report.position, pad))
                print(f"Closest Landpad: {closest_pad.location_x}, {closest_pad.location_y}")

                # Move to the closest landpad
                x_dist = closest_pad.location_x - report.position.location_x
                y_dist = closest_pad.location_y - report.position.location_y
                #print(f"{x_dist}, {y_dist}")
                command = commands.Command.create_set_relative_destination_command(x_dist, y_dist)
                
                self.landpad_reached = True

            else:
                command = commands.Command.create_land_command()

        #raise NotImplementedError

        return command
    
    # Method used to check distance sqaured between two locations
    #   We don't need the square root since this is for comparison only
    def get_distance(self, loc_1: location.Location, loc_2: location.Location):
        # Don't need to square root when comparing between squares
        hypotenuse_squared = (loc_1.location_x - loc_2.location_x) ** 2 + (loc_1.location_y - loc_2.location_y) ** 2
        return hypotenuse_squared
    
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============