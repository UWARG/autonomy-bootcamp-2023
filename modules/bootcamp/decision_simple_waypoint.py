"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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
class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
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

        self.has_sent_landing_command = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    # Function to calculate the square of the Euclidean distance between two Location
    # objects. We use the square of the distance to avoid calculating the square root
    # which is computationally expensive.
    def euclidean_distance_sq(self, loc1: location.Location, loc2: location.Location):
        return (loc1.location_x - loc2.location_x)**2 + (loc1.location_y - loc2.location_y)**2

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

        # NOTE: The second condition here handles the case where the drone
        # can halt at any time. By checking if we're clear to land, i.e, if
        # we've reached the designated waypoint in this case, we can make the
        # appropriate decision.
        if report.status == drone_status.DroneStatus.HALTED:
            distance_to_wp_sq = self.euclidean_distance_sq(self.waypoint, report.position)
            if distance_to_wp_sq <= self.acceptance_radius**2:
                if not self.has_sent_landing_command:
                    # Initiate landing
                    print("Initiating landing...")
                    command = commands.Command.create_land_command()
                    self.has_sent_landing_command = True
            else:
                # Drone can land at the waypoint
                print("Halted at: " + str(report.position))

                # Move to waypoint
                relative_x = self.waypoint.location_x - report.position.location_x
                relative_y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
            
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
