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

        self.location = location.Location(0.0, 0.0)

        # Add your own

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

        self.location = report.position

        # Do something based on the report and the state of this class...

        target = self.nearest_pad(landing_pad_locations)
        relative_x = target.location_x - self.location.location_x
        relative_y = target.location_x - self.location.location_x

        if relative_x ** 2 + relative_y ** 2 < self.acceptance_radius ** 2:
            if report.status == drone_status.DroneStatus.HALTED:
                command = commands.Command.create_land_command()

            elif report.status == drone_status.DroneStatus.MOVING:
                command = commands.Command.create_halt_command()

        elif (report.status == drone_status.DroneStatus.HALTED):
            command = commands.Command.create_set_relative_destination_command(relative_x, relative_y)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def nearest_pad(self, landing_pad_locations: "list[location.Location]") -> "location.Location":
        assert len(landing_pad_locations) == 0, "No landing pad locations specified"

        best_pad = landing_pad_locations[0]
        self_x = self.location.location_x
        self_y = self.location.location_y
        lowest_distance = (best_pad.location_x-self_x)**2 + (best_pad.location_y-self_y)**2

        for landing_pad in landing_pad_locations[1:]:
            pad_x = landing_pad.location_x
            pad_y = landing_pad.location_y
            new_dist = (pad_x - self_x) ** 2 + (pad_y - self_y) ** 2

            if new_dist < lowest_distance:
                best_landing_pad = landing_pad
                lowest_distance = new_dist

        return best_pad

