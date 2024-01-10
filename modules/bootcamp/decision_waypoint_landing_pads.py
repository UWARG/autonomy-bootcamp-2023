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

def pad_distance_squared(pad: location.Location, 
                         drone: location.Location) -> float:
        
        return (pad.location_x - drone.location_x) ** 2 + (pad.location_y - drone.location_y) ** 2

def clamp(number: float,
          min: float,
          max: float) -> float:
    if number < min:
        return min
    if number > max:
        return max
    return number

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

        distance_x = self.waypoint.location_x - report.position.location_x
        distance_y = self.waypoint.location_y - report.position.location_y

        if report.status is drone_status.DroneStatus.HALTED:
            if abs(distance_x) < 0.1 and abs(distance_y) < 0.1:
                if self.reached_waypoint:
                    command = commands.Command.create_land_command()
                else:
                    self.reached_waypoint = True
                    closest_pad = landing_pad_locations[0]
                    closest_pad_distance_squared = float('inf')
                    for landing_pad_location in landing_pad_locations:
                        if pad_distance_squared(landing_pad_location, report.position) < closest_pad_distance_squared:
                            closest_pad_distance_squared = pad_distance_squared(landing_pad_location, report.position)
                            closest_pad = landing_pad_location
                    self.waypoint = closest_pad
            else:
                command = commands.Command.create_set_relative_destination_command(clamp(distance_x, -60, 60), clamp(distance_y, -60, 60))


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
