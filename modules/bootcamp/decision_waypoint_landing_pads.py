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
    staticmethod
    def calculate_closest_location(start_loc: location.Location, loc_list:"list[location.Location]") -> location.Location:
        shortest = float('inf')
        
        for landing_loc in loc_list:
            if DecisionWaypointLandingPads.calculate_distance(start_loc, landing_loc) < shortest:
                shortest = DecisionWaypointLandingPads.calculate_distance(start_loc, landing_loc)
                shortest_location = landing_loc
        
        return shortest_location

    def calculate_distance(loc1: location.Location, loc2: location.Location) -> float:
        return ((loc1.location_x - loc2.location_x) ** 2 + (loc1.location_y - loc2.location_y) ** 2)**0.5

    def calculate_direction(from_loc: location.Location, to_loc: location.Location) -> location.Location:
            """
            Calculate the direction vector from current location to waypoint.
            """
            direction_x = to_loc.location_x - from_loc.location_x
            direction_y = to_loc.location_y - from_loc.location_y
            return location.Location(location_x=direction_x, location_y=direction_y)
    
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
        self.has_started_journey = False
        self.has_reached_waypoint = False
        self.location_closest_landing = 0

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
        distance_to_waypoint = DecisionWaypointLandingPads.calculate_distance(report.position, self.waypoint)
        fly_direction = DecisionWaypointLandingPads.calculate_direction(report.position, self.waypoint)
        if self.has_reached_waypoint:
            distance_to_landing_pad = DecisionWaypointLandingPads.calculate_distance(report.position, self.location_closest_landing)
            if distance_to_landing_pad <= self.acceptance_radius:
                return commands.Command.create_land_command()
            if report.status == drone_status.DroneStatus.MOVING and distance_to_landing_pad <= self.acceptance_radius:
                print('Reaches acceptance_radius, halt the drone')
                return commands.Command.create_halt_command()
        else:
            if report.status == drone_status.DroneStatus.HALTED and not self.has_reached_waypoint:
                if distance_to_waypoint <= self.acceptance_radius:
                    print("Reached Waypoint, Start journey to closest landing pad")
                    self.has_started_journey = False
                    self.has_reached_waypoint = True
                    self.location_closest_landing = DecisionWaypointLandingPads.calculate_closest_location(self.waypoint, landing_pad_locations)
                    fly_direction = DecisionWaypointLandingPads.calculate_direction(report.position, self.location_closest_landing)
                    return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
                elif not self.has_started_journey:
                    print("Haven't started yet, Prepare to start journey")
                    self.has_started_journey = True
                    return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
                else:
                    print('Unexpected halted situation, resume movement')
                    return commands.Command.create_set_relative_destination_command(fly_direction.location_x, fly_direction.location_y)
       
       
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
   