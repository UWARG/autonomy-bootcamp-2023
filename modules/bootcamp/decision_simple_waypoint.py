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

        self.has_sent_move_command = False

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
        if report.status == drone_status.DroneStatus.HALTED:
            if self.has_sent_move_command:
                # Drone has moved to the waypoint
                command = commands.Command.create_land_command()
            else:
                # Drone is at the starting point
                #    Calculate relative destination
                relative_x, relative_y = self.calculate_relative_distance(waypoint=self.waypoint, 
                                                                        drone_location=report.position)
                command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
                print("Drone location:", report.position)
                print("Travelling to", self.waypoint)
                print("Relative Distance is ", relative_x, relative_y)
                self.has_sent_move_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    def calculate_relative_distance(self, 
                                    waypoint: location.Location, 
                                    drone_location: location.Location) -> (float, float):
        """
        Given the absolute location of the waypoint and the drone, return the relative distance of the two
        """
        return (waypoint.location_x - drone_location.location_x, waypoint.location_y - drone_location.location_y)
