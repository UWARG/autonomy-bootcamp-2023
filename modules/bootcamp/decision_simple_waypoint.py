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

        self.action_dict = dict(zip(("MOVE", "HALT", "LAND"), range(3,6)))

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def distance_between_waypoint(self, given_location:location.Location) -> "tuple[float, float]":
        """
        Returns the distance between the given location and waypoint.
        """
        given_loc_from_waypoint_location_x = self.waypoint.location_x - given_location.location_x
        given_loc_from_waypoint_location_y = self.waypoint.location_y - given_location.location_y
        return (given_loc_from_waypoint_location_x, given_loc_from_waypoint_location_y)

    def check_if_near_waypoint(self, given_location:location.Location) -> bool:
        """
        Checks if the given location is on the waypoint by an acceptance radius.
        """
        absolute_acceptance_radius = abs(self.acceptance_radius)
        difference_location_x, difference_location_y = self.distance_between_waypoint(given_location)
        if abs(difference_location_x) < absolute_acceptance_radius and abs(difference_location_y) < absolute_acceptance_radius:
            return True
        return False

    def next_relative_coordinates_to_waypoint(self, given_location:location.Location) -> "tuple[float, float]":
        """
        Returns the relative x and y coordinates for drone to be sent to.
        """
        relative_x, relative_y = self.distance_between_waypoint(given_location)
        return (relative_x, relative_y)

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

        action = None
        report_status = report.status
        report_position = report.position

        if report_status == drone_status.DroneStatus.LANDED:
            action = None
        elif report_status == drone_status.DroneStatus.HALTED:
            if self.check_if_near_waypoint(report_position):
                action = self.action_dict["LAND"]
            else:
                action = self.action_dict["MOVE"]

        if action is None:
            pass
        elif action == self.action_dict["MOVE"]:
            relative_x, relative_y = self.next_relative_coordinates_to_waypoint(report_position)
            command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
        elif action == self.action_dict["HALT"]:
            command = commands.Command.create_halt_command()
        elif action == self.action_dict["LAND"]:
            command = commands.Command.create_land_command()

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
