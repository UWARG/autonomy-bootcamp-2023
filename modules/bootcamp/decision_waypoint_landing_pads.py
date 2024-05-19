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
        self.halt_at_init_pos = True
        self.halt_at_waypoint = False
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
        if report.status == drone_status.DroneStatus.HALTED and self.halt_at_init_pos:
            self.halt_at_init_pos = False
            self.halt_at_waypoint = True 
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, 
                                                                               self.waypoint.location_y)
        elif report.status == drone_status.DroneStatus.HALTED and not self.halt_at_init_pos and self.halt_at_waypoint:
            self.halt_at_waypoint = False 
            max_dist_squared = float('inf')

            for cur_landing_pad in landing_pad_locations:
                cur_dist_squared = pow((self.waypoint.location_x - 
                    cur_landing_pad.location_x), 2) + pow((self.waypoint.location_y - 
                    cur_landing_pad.location_y), 2)
                if cur_dist_squared < max_dist_squared:
                    max_dist_squared = cur_dist_squared
                    self.closest_landing_pad = cur_landing_pad
            
            command = commands.Command.create_set_relative_destination_command(self.closest_landing_pad.location_x 
                        - self.waypoint.location_x, self.closest_landing_pad.location_y - self.waypoint.location_y)
        elif report.status == drone_status.DroneStatus.HALTED and not self.halt_at_init_pos and not self.half_at_waypoint:
            command = commands.Command.create_land_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command