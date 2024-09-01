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

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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

        # Do something based on the report and the state of this class...

        # Remove this when done
        # raise NotImplementedError

        # get_distance returns the straight line distances between the position and destination
        def get_distance(x_dist, y_dist):

            distance = (x_dist ** 2 + y_dist ** 2) ** 0.5

            return distance
        
        relative_x = self.waypoint.location_x - report.position.location_x
        relative_y = self.waypoint.location_y - report.position.location_y
        distance = get_distance(relative_x, relative_y)

        if report.status == drone_status.DroneStatus.HALTED:
            # If halted && in acceptance radius, then land
            if distance < self.acceptance_radius:
                command = commands.Command.create_land_command()
            # If not in acceptance radius, then fly to destination
            else:
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

        if report.status == drone_status.DroneStatus.MOVING:
            # If moving && in acceptance radius, then halt
            if distance < self.acceptance_radius:
                command = commands.Command.create_halt_command()
            # If not, then do nothing and keep moving
        
        # If status is landed - do nothing - should only happen at destination

        # no need to use landing_pad_locations

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
