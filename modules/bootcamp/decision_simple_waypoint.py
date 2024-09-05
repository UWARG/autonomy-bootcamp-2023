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

        # Add your own
        self.waypoint_reached = False
        self.waypoint_reached_count = 0
        self.waypoint_landed = False 

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def distance_to_waypoint(self, report: drone_report.DroneReport) -> float:
        """
        Calculate the distance between the drone and the waypoint (in pixels - returns the maximum of the x and y distances).
        """
        drone_location = report.position
        return ((drone_location.location_x - self.waypoint.location_x)**2 + (drone_location.location_y - self.waypoint.location_y)**2) ** (1/2)

    def get_relative_displacement(self, report: drone_report.DroneReport) -> location.Location:
        """
        Calculate the relative displacement between the drone and the waypoint.
        """
        drone_location = report.position
        return location.Location(self.waypoint.location_x - drone_location.location_x, self.waypoint.location_y - drone_location.location_y)

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

        # drone is moving to whatever position we put
        if report.status == drone_status.DroneStatus.MOVING:
            # if the drone is moving, we don't need to do anything
            # print(report.position)
            # print(self.waypoint)
            return command 

        # if waypoint is reached, we land
        if self.waypoint_reached:
            print("Landing")
            self.waypoint_landed = True
            return commands.Command.create_land_command()

        # checks if the drone is within the acceptance radius
        print(self.distance_to_waypoint(report))
        print(self.acceptance_radius)
        print("----------------")
        if self.distance_to_waypoint(report) <= self.acceptance_radius:
            print("Waypoint reached")
            self.waypoint_reached = True
            command = commands.Command.create_halt_command()
            return command

        # if not moving and none of the above, we take off
        if report.status == drone_status.DroneStatus.HALTED and not self.waypoint_reached:
            print("Moving to waypoint")

            relative_destination_from_current_position = self.get_relative_displacement(report)
            command = commands.Command.create_set_relative_destination_command(
                relative_destination_from_current_position.location_x,
                relative_destination_from_current_position.location_y
            )
        # return command
        


        # # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
