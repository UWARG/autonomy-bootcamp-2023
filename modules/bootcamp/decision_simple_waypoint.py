"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""


from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision

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
        self.acceptance_radius_sqr = self.acceptance_radius ** 2


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
        command = commands.Command.create_null_command()
        
        if report.status == drone_status.DroneStatus.HALTED:
            current_pos = report.position
            distance_sqr = (self.waypoint.location_x - current_pos.location_x) ** 2 + (self.waypoint.location_y - current_pos.location_y) ** 2
            if distance_sqr <= self.acceptance_radius_sqr:
                command = commands.Command.create_land_command()
            else:
                relative_x = self.waypoint.location_x - current_pos.location_x
                relative_y = self.waypoint.location_y - current_pos.location_y
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

        return command
