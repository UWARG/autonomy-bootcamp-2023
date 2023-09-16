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

        self.action_dict = dict(zip(("MOVE", "HALT", "LAND"), range(3,6)))
        self.origin = location.Location(0,0)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def shortest_distance(target_location:location.Location, given_location:location.Location) -> float:
            """
            Finds out the shortest distance between two given locations.
            """
            x_1, y_1 = given_location.location_x, given_location.location_y
            x_2, y_2 = target_location.location_x, target_location.location_y
            x_square = (x_2 - x_1) ** 2
            y_square = (y_2 - y_1) ** 2
            return (x_square + y_square) ** 0.5
    
    def relative_coordinates_of_target(self, target_location:location.Location, given_location:location.Location) -> "tuple[float, float]":
        """
        Returns the relative coordinates of target w.r.t given location.
        """
        relative_location_x = target_location.location_x - given_location.location_x
        relative_location_y = target_location.location_y - given_location.location_y
        return (relative_location_x, relative_location_y)

    def check_if_near_target(self, target_location:location.Location, given_location:location.Location) -> bool:
        """
        Checks if the given location is near the target by an acceptance radius.
        """
        absolute_acceptance_radius = abs(self.acceptance_radius)
        difference_location_x, difference_location_y = self.relative_coordinates_of_target(target_location, given_location)
        if abs(difference_location_x) < absolute_acceptance_radius and abs(difference_location_y) < absolute_acceptance_radius:
            return True
        return False

    def next_relative_coordinates_to_target(self,
                                            target_location:location.Location,
                                            given_location:location.Location) -> "tuple[float, float]":
        """
        Returns the relative x and y coordinates for drone to be sent to.
        """
        relative_x, relative_y = self.relative_coordinates_of_target(target_location, given_location)
        divider = 1
        if abs(relative_x) > abs(relative_y):
            return (relative_x/divider, relative_y)
        elif abs(relative_x) < abs(relative_y):
            return (relative_x, relative_y/divider)
        else:
            return (relative_x/divider, relative_y/divider)

    def closest_landing_pad(self,
                            given_location:location.Location,
                            landing_pad_locations: "list[location.Location]") -> location.Location:
        """
        Finds out the closest landing pad from the given location by checking out their distances.
        """
        closest_location = landing_pad_locations[0]
        for landing_pad in landing_pad_locations[1:]:
            distance_from_given_location = DecisionWaypointLandingPads.shortest_distance(landing_pad, given_location)
            distance_from_closest_location = DecisionWaypointLandingPads.shortest_distance(closest_location, given_location)
            if distance_from_given_location < distance_from_closest_location:
                closest_location = landing_pad
        return closest_location


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

        action = None
        report_status = report.status
        report_position = report.position
        target = self.waypoint

        if report_status == drone_status.DroneStatus.HALTED:
            landing_pad = self.closest_landing_pad(self.waypoint, landing_pad_locations)
            action = self.action_dict["MOVE"]
            if self.check_if_near_target(self.waypoint, report_position):
                target = landing_pad
            if (self.check_if_near_target(landing_pad, report_position)
                and (DecisionWaypointLandingPads.shortest_distance(self.waypoint, report_position) - DecisionWaypointLandingPads.shortest_distance(self.waypoint, landing_pad) < 0.1)
                and (
                    (self.check_if_near_target(landing_pad, self.origin) and self.check_if_near_target(self.waypoint, self.origin))
                    or (not self.check_if_near_target(report_position, self.origin))
                )):
                """ 
                self.check_if_near_target(landing_pad, self.origin) - if nearest landing pad is origin
                self.check_if_near_target(self.waypoint, self.origin) - if waypoint is origin
                self.check_if_near_target(report_position, self.origin) - if current position is origin
                """
                action = self.action_dict["LAND"]

        if action is None:
            pass
        elif action == self.action_dict["MOVE"]:
            relative_x, relative_y = self.next_relative_coordinates_to_target(target, report_position)
            command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)
        elif action == self.action_dict["HALT"]:
            command = commands.Command.create_halt_command()
        elif action == self.action_dict["LAND"]:
            command = commands.Command.create_land_command()


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
