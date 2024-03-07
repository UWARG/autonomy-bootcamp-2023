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

        self.at_home = True

        # Once Waypoint is reached we are not at the local landing pad
        self.at_local_pad = False

        # Variable to find the distance from a pad and to record the closest pad
        self.distance = float('inf')
        self.closest_pad = 0
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
        
        for i in landing_pad_locations:
            if (((i.location_x - report.position.location_x) ** 2) + ((i.location_y - report.position.location_y) ** 2)) < self.distance:
                self.closest_pad = i

        if report.status == drone_status.DroneStatus.HALTED and self.at_home == True:
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)
            self.at_home = False

        elif report.status == drone_status.DroneStatus.HALTED and self.at_home == False:

            command = commands.Command.create_set_relative_destination_command(self.closest_pad.location_x - report.position.location_x, self.closest_pad.location_y - report.position.location_y)
            self.at_local_pad = True

        elif report.status == drone_status.DroneStatus.HALTED and self.at_local_pad == True:
            command = commands.Command.create_land_command()
        """   
            if report.position.location_x == self.waypoint.location_x and report.position.location_y == self.waypoint.location_y and self.at_local_pad == False:
                command = commands.Command.create_set_relative_destination_command(closest_pad.location_x - report.position.location_x, closest_pad.location_y - report.position.location_y)
                self.at_local_pad = True

            else:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)
        """

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command