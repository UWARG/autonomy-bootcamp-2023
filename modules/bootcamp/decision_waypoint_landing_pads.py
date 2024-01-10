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
        self.away_from_landing_pad = False
        self.away_from_waypoint = False

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

        def distance_between_locations(location_one: location.Location, location_two: location.Location):
            return ((location_one.location_x - location_two.location_x)**2 + (location_one.location_y - location_two.location_y)**2)**0.5
        
        status = report.status
        halted = drone_status.DroneStatus.HALTED
        # Do something based on the report and the state of this class...

        if status == halted:
            # Case 1: moving to the waypoint
            if not self.away_from_landing_pad and not self.away_from_waypoint:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)
                self.away_from_landing_pad = True

            # Case 2: moving to the nearest landing pad only when at waypoint
            elif not self.away_from_waypoint and self.away_from_landing_pad:
                nearest_pad = landing_pad_locations[0]
                min_dist = distance_between_locations(self.waypoint, nearest_pad)
                for pad in landing_pad_locations[1:]:
                    dist = distance_between_locations(self.waypoint, pad)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_pad = pad
                command = commands.Command.create_set_relative_destination_command(nearest_pad.location_x - report.position.location_x, nearest_pad.location_y - report.position.location_y)
                self.away_from_waypoint = True

            # Case 3: land only when arrived at landing pad
            elif self.away_from_landing_pad and self.away_from_waypoint:
                command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
