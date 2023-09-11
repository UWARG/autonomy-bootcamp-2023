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

        self.waypointReached = False
        self.targetSet = False
        self.target = None
        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    @staticmethod
    def getDistance(a: location.Location, b: location.Location) -> float:
        """
        Get the distance between two locations.
        """
        return ((a.location_x-b.location_x)**2 + (a.location_y-b.location_y)**2)**0.5

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
        if (report.status == drone_status.DroneStatus.MOVING and not self.waypointReached):
            if (DecisionWaypointLandingPads.getDistance(report.position,self.waypoint)<self.acceptance_radius):
                command = commands.Command.create_halt_command()
        elif (report.status == drone_status.DroneStatus.HALTED and not self.waypointReached):
            if (DecisionWaypointLandingPads.getDistance(report.position,self.waypoint)<self.acceptance_radius):
                self.waypointReached = True
                command = commands.Command.create_halt_command()
            else:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
        elif (self.waypointReached):
            if (not self.targetSet):
                closestTarget = None

                for target in landing_pad_locations:
                    if (closestTarget == None):
                        closestTarget = target
                    elif (DecisionWaypointLandingPads.getDistance(report.position, target) < DecisionWaypointLandingPads.getDistance(report.position, closestTarget)):
                        closestTarget = target
                self.target = closestTarget
                self.targetSet = True
            else:
                if (report.status == drone_status.DroneStatus.MOVING):
                    if (DecisionWaypointLandingPads.getDistance(report.position,self.target)<self.acceptance_radius):
                        command = commands.Command.create_halt_command()
                elif (report.status == drone_status.DroneStatus.HALTED):
                    if (DecisionWaypointLandingPads.getDistance(report.position,self.target)<self.acceptance_radius):
                        command = commands.Command.create_land_command()
                    else:
                        command = commands.Command.create_set_relative_destination_command(self.target.location_x-report.position.location_x, self.target.location_y-report.position.location_y)
                else:
                    command = commands.Command.create_null_command()
        else:
             command = commands.Command.create_null_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
