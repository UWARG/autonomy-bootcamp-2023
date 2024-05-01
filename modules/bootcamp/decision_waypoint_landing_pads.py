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

        # Keeping track of what stage the drone is at:
        self.at_pad = True
        self.at_waypoint = False

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

        # Finds the closest landing pad to the drone's current location:
        def distance_to_pad_sqr(pad_loc: location.Location, drone_loc: location.Location) -> float:
            distance_sqr = ((drone_loc.location_x - pad_loc.location_x) ** 2 +
                            (drone_loc.location_y - pad_loc.location_y) ** 2)
            return distance_sqr

        # While the status is HALTED:
        if report.status == drone_status.DroneStatus.HALTED:
            # Task 1: Move from initial position to waypoint.
            #   at initial pad
            #   not at final waypoint
            if self.at_pad and not self.at_waypoint:
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x,
                    self.waypoint.location_y - report.position.location_y)
                self.at_pad = False
                self.at_waypoint = True
            # Task 2: Move from waypoint to the closest landing pad.
            #   not at initial pad
            #   at final waypoint
            elif not self.at_pad and self.at_waypoint:
                # Finding the closest landing pad location:
                best_pad = landing_pad_locations[0]
                best_dist_sqr = distance_to_pad_sqr(best_pad, self.waypoint)
                for this_location in landing_pad_locations[1:]:
                    this_dist_sqr = distance_to_pad_sqr(this_location, self.waypoint)
                    if this_dist_sqr < best_dist_sqr:
                        best_pad = this_location
                        best_dist_sqr = this_dist_sqr
                # Move to the closest landing pad:
                command = commands.Command.create_set_relative_destination_command(
                    best_pad.location_x - report.position.location_x,
                    best_pad.location_y - report.position.location_y
                )
                self.at_waypoint = False
            # Task 3: Land.
            #   not at initial pad
            #   not at final waypoint
            elif not self.at_pad and not self.at_waypoint:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
