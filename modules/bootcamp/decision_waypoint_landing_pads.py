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
        self.reached_waypoint = False
        self.destination = waypoint

        # Validate data
        if abs(self.waypoint.location_x) > 60 or abs(self.waypoint.location_y) > 60:
            print("Invalid waypoint, must be in flight boundary")
    

    def euclidean_distance_squared(self, x0: float, y0: float, x1: float, y1: float) -> float:
        return (x1-x0)**2 + (y1-y0)**2
    

    def get_closest_landing_pad(self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]") -> location.Location:
        closest_distance_to_landing_squared = float('inf')
        closest_landing_location = landing_pad_locations[0]

        for location in landing_pad_locations:
            distance_to_landing_squared = self.euclidean_distance_squared(
                location.location_x, location.location_y, 
                report.position.location_x, report.position.location_y)

            if distance_to_landing_squared < closest_distance_to_landing_squared:
                closest_landing_location = location
                closest_distance_to_landing_squared = distance_to_landing_squared
        return closest_landing_location


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

        # New commands need to be sent only when automatically halted
        if report.status == drone_status.DroneStatus.HALTED:
            # Only compute distance if needed within halt branch
            distance_to_destination_squared = self.euclidean_distance_squared(
                report.position.location_x, report.position.location_y, 
                self.destination.location_x, self.destination.location_y)

            # Reached the destination
            if distance_to_destination_squared < self.acceptance_radius**2:
                # Accounts for the case when waypoint is on landing pad and/or when reaching landing pad
                if self.reached_waypoint or self.waypoint in landing_pad_locations:
                    return commands.Command.create_land_command()

                # find location of closest launch pad
                closest_landing_location = self.get_closest_landing_pad(report, landing_pad_locations)

                # Change waypoint to closest landing pad (simplifes number of distance calculations)
                self.destination = closest_landing_location
                self.reached_waypoint = True

            else:
                # At the starting point or at first waypoint, set new relative destination
                return commands.Command.create_set_relative_destination_command(
                    self.destination.location_x - report.position.location_x,
                    self.destination.location_y - report.position.location_y)


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
