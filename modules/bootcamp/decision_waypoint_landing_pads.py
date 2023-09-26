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

        self.begin = True
        self.reached_waypoint = False

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

        closest_landing_pad = landing_pad_locations[0]

        # Do something based on the report and the state of this class...
        if self.begin and report.status == drone_status.DroneStatus.HALTED:
            print("setting waypoint")
            self.begin = False
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x  - report.position.location_x, self.waypoint.location_y  - report.position.location_y)
        
        elif not self.reached_waypoint and self.within_range(self.waypoint, report.position) and report.status == drone_status.DroneStatus.MOVING:
            print("halting at waypoint: ", str(report.position))
            self.reached_waypoint = True
            command = commands.Command.create_halt_command()

        elif self.reached_waypoint and self.within_range(self.waypoint, report.position) and report.status == drone_status.DroneStatus.HALTED:
            print("finding closest landing pad")
            closest_distance = DecisionWaypointLandingPads.calculate_distance(landing_pad_locations[0],report.position)

            for i in range (1, len(landing_pad_locations)):
                distance = DecisionWaypointLandingPads.calculate_distance(landing_pad_locations[i],report.position)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_landing_pad = landing_pad_locations[i]
                
            if self.within_range(closest_landing_pad, report.position):
                print("landing at landing pad: ", str(report.position))
                command = commands.Command.create_land_command()

            command = commands.Command.create_set_relative_destination_command(
                closest_landing_pad.location_x - report.position.location_x, 
                closest_landing_pad.location_y - report.position.location_y
            )

        elif self.reached_waypoint and self.within_range(closest_landing_pad, report.position) and report.status == drone_status.DroneStatus.MOVING:
            print("halting at landing pad: ", str(report.position))
            command = commands.Command.create_halt_command()

        elif self.reached_waypoint and self.within_range(closest_landing_pad, report.position) and report.status == drone_status.DroneStatus.HALTED:
            print("landing at landing pad: ", str(report.position))
            command = commands.Command.create_land_command()

        else:
            print("just moving")
        # Remove this when done

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    @staticmethod
    def calculate_distance(l1: location.Location, l2: location.Location) -> float:
        return (l1.location_x - l2.location_x) ** 2 + (l1.location_y - l2.location_y) ** 2
    
    def within_range(self, l1: location.Location, l2: location.Location,) -> bool:
        return (abs(l1.location_x - l2.location_x)) < self.acceptance_radius and (abs(l1.location_y - l2.location_y)) < self.acceptance_radius
