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
import math


# Disable for bootcamp use
# pylint: disable=unused-argument,line-too-long

def euclidean_distance(a: location.Location, b: location.Location):
    return math.sqrt((a.location_x - b.location_x)**2 + (a.location_y - b.location_y)**2)


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
        self.waypoint_command = commands.Command.create_set_relative_destination_command(
            waypoint.location_x,
            waypoint.location_y
        )
        
        # Let:
        # stage = 0 be going to the waypoint, 
        # stage = 1 be going to the landing pad, 
        # stage = 2 be landing
        self.stage = 0

        self.counter = 0

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
        # First, need to fly to waypoint
        if report.status == drone_status.DroneStatus.HALTED and self.stage == 0:
            command = self.waypoint_command
            # Proceed to next stage
            self.stage += 1

        # Then, need to find the nearest landing pad and go there
        elif report.status == drone_status.DroneStatus.HALTED and self.stage == 1:
            # Find closest landing pad
            min_dist = euclidean_distance(report.position, landing_pad_locations[0])
            closest_landing_pad = landing_pad_locations[0]

            for landing_pad_location in landing_pad_locations[1:]:
                new_dist = euclidean_distance(report.position, landing_pad_location)
                if new_dist < min_dist:
                    closest_landing_pad = landing_pad_location
                    min_dist = new_dist
            
            # Send the command to go to landing pad
            command = commands.Command.create_set_relative_destination_command(
                closest_landing_pad.location_x - report.position.location_x,
                closest_landing_pad.location_y - report.position.location_y
            )
            # Proceed to next stage
            self.stage += 1
        
        # Finally, land the drone
        elif report.status == drone_status.DroneStatus.HALTED and self.stage == 2:
            command = commands.Command.create_land_command()
            # Finish (won't run anymore commands)
            self.stage += 1

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
