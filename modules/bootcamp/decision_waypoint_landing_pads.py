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
        self.started = False
        self.located_pad = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============


    def get_nearest_landing_pad(self,
                                landing_pad_locations: "list[location.Location]",
                                waypoint: location.Location) -> location.Location:
        min_dist = float("inf")
        desired_location = landing_pad_locations[0]

        for pad in landing_pad_locations:
            distance = ((waypoint.location_x - pad.location_x) ** 2 + (
                        waypoint.location_y - pad.location_y) ** 2) ** 0.5

            if distance < min_dist:
                min_dist = distance
                desired_location = pad

        return desired_location

    def within_tolerance(self,
                         curr: location.Location,
                         dest: location.Location) -> bool:

        if abs(dest.location_x - curr.location_x) > self.acceptance_radius:
            return False

        if abs(dest.location_y - curr.location_y) > self.acceptance_radius:
            return False

        return True

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

        # if drone is at a waypoint
        if self.started and self.within_tolerance(report.position, report.destination):
            command = commands.Command.create_halt_command()
            print("stopped")
            if drone_status.DroneStatus.HALTED == report.status:
                if not self.located_pad and self.within_tolerance(report.position, report.destination):
                    print("checking nearest distance")
                    self.waypoint = self.get_nearest_landing_pad(landing_pad_locations, self.waypoint)
                    self.located_pad = True
                    self.started = False
                else:
                    print("trying to land")
                    command = commands.Command.create_land_command()

        # if drone has not left waypoint
        if report.status == drone_status.DroneStatus.HALTED and not self.started:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x,
                self.waypoint.location_y - report.position.location_y)
            self.started = True
            print("moving")
        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
