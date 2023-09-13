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

        self.has_left_home = False
        self.has_left_waypoint = False

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

        # Do something based on the report and the state of this class...

        # Helper function to calculate distance between two points
        def distance_between_points(current_location: location.Location, destination_location: location.Location) -> float:
            x1 = current_location.location_x
            y1 = current_location.location_y
            x2 = destination_location.location_x
            y2 = destination_location.location_y

            return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        
        # Helper function to calculate relative destination
        def relative_destination(current_location: location.Location, destination_location: location.Location) -> location.Location:
            x1 = current_location.location_x
            y1 = current_location.location_y
            x2 = destination_location.location_x
            y2 = destination_location.location_y

            return location.Location(x2 - x1, y2 - y1)

        # If the drone is not at the waypoint, move to the waypoint
        if report.status == drone_status.DroneStatus.HALTED and not self.has_left_home and not self.has_left_waypoint:
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)
            self.has_left_home = True

        # If the drone is at the waypoint, move to the nearest landing pad
        elif report.status == drone_status.DroneStatus.HALTED and self.has_left_home and not self.has_left_waypoint:
            closest_landing_pad = landing_pad_locations[0]
            closest_pad_dist = distance_between_points(self.waypoint, closest_landing_pad)

            # Check if the below works
            for landing_pad in landing_pad_locations[1:]:
                if distance_between_points(self.waypoint, landing_pad) < closest_pad_dist:
                    closest_landing_pad = landing_pad
                    closest_pad_dist = distance_between_points(self.waypoint, landing_pad)
            
            destination_to_landing_pad = relative_destination(report.position, closest_landing_pad)
            command = commands.Command.create_set_relative_destination_command(destination_to_landing_pad.location_x, destination_to_landing_pad.location_y)
            self.has_left_waypoint = True

        # If the drone is at the landing pad, land
        elif report.status == drone_status.DroneStatus.HALTED and self.has_left_home and self.has_left_waypoint:
            command = commands.Command.create_land_command()

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
