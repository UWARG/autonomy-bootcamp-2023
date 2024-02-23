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

        # Error checking of `waypoint`
        if (waypoint.location_x < -60 or waypoint.location_x > 60) or \
            (waypoint.location_y < -60 or waypoint.location_y > 60):
            # Ideally, an exception should be raised, but for purposes of
            # the bootcamp, we've been asked to refrain from doing so.
            print("Invalid waypoint provided.")

        self.closest_lp = None
        self.reached_waypoint = False
        self.has_sent_landing_command = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    # Function to calculate the square of the Euclidean distance between two Location
    # objects. We use the square of the distance to avoid calculating the square root
    # which is computationally expensive.
    # This function is rather unnecessary because we only calculate the distance once
    # here, but it's good practice to do it this way.
    def euclidean_distance_sq(self, loc1: location.Location, loc2: location.Location):
        return (loc1.location_x - loc2.location_x)**2 + (loc1.location_y - loc2.location_y)**2

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

        # Determine target based on whether the waypoint has been reached
        if not self.reached_waypoint:
            target = self.waypoint
        else:
            # Ensure there's a closest landing pad selected
            if self.closest_lp is None:
                assert len(landing_pad_locations) > 0  # Ensure there's at least one landing pad
                self.closest_lp = min(landing_pad_locations, key=lambda lp: self.euclidean_distance_sq(self.waypoint, lp))
            target = self.closest_lp

        if report.status == drone_status.DroneStatus.HALTED:
            distance_to_target_sq = self.euclidean_distance_sq(target, report.position)
            # Check if within acceptable range to land or move closer
            if distance_to_target_sq <= self.acceptance_radius**2:
                if not self.reached_waypoint:
                    self.reached_waypoint = True  # For waypoint, next iteration will handle landing.
                    print("Reached waypoint, preparing for next steps.")
                else:
                    # For landing pad, land immediately.
                    command = commands.Command.create_land_command()
                    print("Landing at the closest landing pad at ", self.closest_lp)
            else:
                # Move towards the target (waypoint or landing pad)
                command = commands.Command.create_set_relative_destination_command(
                    target.location_x - report.position.location_x,
                    target.location_y - report.position.location_y
                )
                print(f"Moving towards {'waypoint' if not self.reached_waypoint else 'landing pad'}.")

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
