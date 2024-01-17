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
        self.at_initial_position = True
        self.going_to_pad = False

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
        
        if drone_status.DroneStatus.HALTED == report.status:
            if self.at_initial_position:
                command = self.set_destination
                self.at_initial_position = False
            
            elif not self.going_to_pad:
                self.going_to_pad = True
                if self.waypoint not in landing_pad_locations:
                    landing_pad = self.find_closest_landing_pad(report.position, landing_pad_locations)
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

    # =======================
    # Helper Functions:
    # =======================
    def find_distance(self, location_one, location_two):
        return (location_two.location_x - location_one.location_x)**2 + (location_two.location_y - location_one.location_y)**2
        
    def find_closest_landing_pad(self, curr_location, landing_pad_list):
        closest_landing_pad = None
        closest_distance = float('inf')
        for landing_pad in landing_pad_list:
            distance = self.find_distance(landing_pad, curr_location)
            if closest_distance > distance:
                closest_distance = distance
                closest_landing_pad = landing_pad
        return closest_landing_pad 
