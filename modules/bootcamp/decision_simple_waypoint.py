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
        self.now_landing = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def within_pad_range(self, position: location.Location) -> bool:
        """
        Checks if the position of the drone is within the acceptable_radius of the waypoint.

        position: The current position of the drone.

        Return: A boolean representing if the drone is within the range or not.
        """
        distance_x = self.waypoint.location_x - position.location_x
        distance_y = self.waypoint.location_y - position.location_y
        distance_from_pad_sqr = distance_x ** 2 + distance_y ** 2
        if distance_from_pad_sqr <= self.acceptance_radius ** 2:
            return True
        
        return False

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

        # status = report.status
        # print(report.status.value)
        within_pad_range = self.within_pad_range(report.position)
        # print(str(report.destination))

        if self.now_landing:
            # Once the drone is landed, we don't need to give it any more commands.
            return command

        elif within_pad_range and report.status == drone_status.DroneStatus.MOVING:
            # If we are within the pad range and the drone is still moving, we want to halt the
            #     drone.
            command = commands.Command.create_halt_command()
        
        elif within_pad_range and report.status == drone_status.DroneStatus.HALTED:
            # If we have halted and are above the pad, we want to start landing.

            print("Halted At: " + str(report.position))
            # print("Waypoint At: " + str(self.waypoint))
            command = commands.Command.create_land_command()
            self.now_landing = True
            # print("Landed")
        
        elif report.status == drone_status.DroneStatus.HALTED:
            # if we are halted, this means we are at the beginning so we tell the drone to start
            #     moving towards the waypoint.

            print("Halted At: " + str(report.position))
            difference_x = self.waypoint.location_x - report.position.location_x
            difference_y = self.waypoint.location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(difference_x, 
                                                                               difference_y)
            # print("Moving: (" + str(difference_x) + ", " + str(difference_y) + ")")

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
