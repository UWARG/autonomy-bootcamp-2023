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
        self.reachedWayPoint = False
        self.toLandAt = waypoint # Initializing to waypoint

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

        position_x, position_y = report.position.location_x, report.position.location_y

        if self.reachedWayPoint:
            destination_x, destination_y = self.toLandAt.location_x, self.toLandAt.location_y
        else:
            destination_x, destination_y = self.waypoint.location_x, self.waypoint.location_y
            
        to_travel_x = destination_x - position_x
        to_travel_y = destination_y - position_y

        #Restricting to flight boundary
        if to_travel_x > 60:
            to_travel_x = 60
        elif to_travel_x < -60:
            to_travel_x = -60
        
        if to_travel_y > 60:
            to_travel_y = 60
        elif to_travel_y < -60:
            to_travel_y = -60

        # Do something based on the report and the state of this class...
        if abs(to_travel_x) <= self.acceptance_radius and abs(to_travel_y) <= self.acceptance_radius:
            if self.reachedWayPoint and report.status == drone_status.DroneStatus.MOVING:
                command = commands.Command.create_halt_command()
            elif self.reachedWayPoint and report.status == drone_status.DroneStatus.HALTED:
                command = commands.Command.create_land_command()
            else:
                self.reachedWayPoint = True
                minimumDistance = float("inf")

                # Iterate through landing pad locations to find closest
                for landing_pad in landing_pad_locations:
                    distance = self.distance(report.position, landing_pad)
                    if distance < minimumDistance:
                        minimumDistance = distance
                        self.toLandAt = landing_pad
                command = commands.Command.create_halt_command()
        elif report.status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_set_relative_destination_command(to_travel_x, to_travel_y)

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    def distance(self, start, end):
        distance_x = end.location_x - start.location_x
        distance_y = end.location_y - start.location_y
        return distance_x**2 + distance_y**2
