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
        self.waypoint_success = False
        # Storing the landing pad and whether the pad has reached:
        self.landing_pad = None
        self.landing_pad_success = False

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

        # If the status is HALTED:
        if report.status == drone_status.DroneStatus.HALTED:
            # If the drone has not reached the waypoint yet:
            if not self.waypoint_success:
                dist_to_waypoint_sqr = ((report.position.location_x - self.waypoint.location_x) ** 2 +
                                        (report.position.location_y - self.waypoint.location_y) ** 2)
                # If the drone is sufficiently close to the waypoint:
                if dist_to_waypoint_sqr <= self.acceptance_radius ** 2:
                    self.waypoint_success = True
                    # Calculate and store the nearest landing pad:
                    best_pad = None
                    best_dist_sqr = float('inf')
                    for this_location in landing_pad_locations:
                        this_dist_sqr = ((this_location.location_x - report.position.location_x) ** 2 +
                                         (this_location.location_y - report.position.location_y) ** 2)
                        if this_dist_sqr < best_dist_sqr:
                            best_pad = this_location
                            best_dist_sqr = this_dist_sqr
                    # Store the nearest landing pad:
                    self.landing_pad = best_pad
                # Otherwise travel to the waypoint:
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y
                    )
            # Otherwise if waypoint has already been reached:
            else:
                dist_to_landing_sqr = ((report.position.location_x - self.landing_pad.location_x) ** 2 +
                                       (report.position.location_y - self.landing_pad.location_y) ** 2)
                # If sufficiently close to the landing pad, land:
                if dist_to_landing_sqr <= self.acceptance_radius ** 2:
                    self.landing_pad_success = True
                    command = commands.Command.create_land_command()
                # Otherwise go to the landing pad:
                else:
                    command = commands.Command.create_set_relative_destination_command(
                        self.landing_pad.location_x - report.position.location_x,
                        self.landing_pad.location_y - report.position.location_y
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
