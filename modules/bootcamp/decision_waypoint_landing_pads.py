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

        self.waypointComplete = False

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

        if self.waypointComplete:
            # Land at nearest landing pad
            position = report.position
            landing_pad = self.findNearestLandingPad(position, landing_pad_locations)

            if report.status == drone_status.DroneStatus.HALTED:
                # If the drone is halted, send it to the landing pad.
                if self.getRelativeDistance(position, landing_pad) > self.acceptance_radius:
                    report.destination = landing_pad
                    command = commands.Command.create_set_relative_destination_command(landing_pad.location_x - position.location_x, landing_pad.location_y - position.location_y)
                else:
                    command = commands.Command.create_land_command()
            elif report.status == drone_status.DroneStatus.MOVING:
                # If the drone is moving, check if it is close enough to the landing pad.
                if self.getRelativeDistance(position, landing_pad) < self.acceptance_radius:
                    command = commands.Command.create_halt_command()
        else:
            # Travel to waypoint
            position = report.position

            if report.status == drone_status.DroneStatus.HALTED:
                # If the drone is halted, send it to the waypoint.
                if self.getRelativeDistance(position, self.waypoint) > self.acceptance_radius:
                    command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - position.location_x, self.waypoint.location_y - position.location_y)
            elif report.status == drone_status.DroneStatus.MOVING:
                # If the drone is moving, check if it is close enough to the waypoint.
                if self.getRelativeDistance(position, self.waypoint) < self.acceptance_radius:
                    command = commands.Command.create_halt_command()
                    self.waypointComplete = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    def findNearestLandingPad(self, position: location.Location, landing_pad_locations: "list[location.Location]") -> location.Location:
        """
        Returns the nearest landing pad to the drone.
        """
        nearestLandingPad = landing_pad_locations[0]
        nearestDistance = self.getRelativeDistance(position, nearestLandingPad)
        for landingPad in landing_pad_locations:
            distance = self.getRelativeDistance(position, landingPad)
            if distance < nearestDistance:
                nearestLandingPad = landingPad
                nearestDistance = distance
        return nearestLandingPad

    def getRelativeDistance(self, position: location.Location, destination: location.Location) -> float:
        """
        Returns the distance between the drone and the waypoint.
        """
        return ((position.location_x - destination.location_x)**2 + (position.location_y - destination.location_y)**2)**0.5