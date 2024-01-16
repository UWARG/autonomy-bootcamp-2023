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
        self.currently_landing = False
        self.set_destination = commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)
        self.count = 0
        self.landed = False

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
        def find_distance(l1: location.Location, l2: location.Location) -> float:
            return (l2.location_x - l1.location_x)*(l2.location_x - l1.location_x) + (l2.location_y - l1.location_y)*(l2.location_y - l1.location_y)
        
        def find_closest_landing_pad(curr_location: location.Location, landing_pads: "list[location.Location]") -> location.Location:
            closest_landing_pad = None
            closest_distance = 10000000000000
            for index in landing_pads:
                distance = find_distance(index, curr_location)
                if closest_distance > distance:
                    closest_distance = distance
                    closest_landing_pad = index
            return closest_landing_pad 
        
        if drone_status.DroneStatus.HALTED == report.status:
            if 0 >= self.count:
                command = self.set_destination
                self.count += 1
            
            elif not self.landed:
                self.landed = True
                if self.waypoint not in landing_pad_locations:
                    landing_pad = find_closest_landing_pad(report.position, landing_pad_locations)
                    command = commands.Command.create_set_relative_destination_command (landing_pad.location_x - report.position.location_x, landing_pad.location_y - report.position.location_y)

            elif not self.currently_landing:
                self.currently_landing = True
                command = commands.Command.create_land_command()

        # Remove this when done
        #raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
