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

        self.acceptance_radius = acceptance_radius ** 2

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own
        self.at_waypoint = False
        self.begin_landing = False

    def at_location(self, cur: location.Location, dest: location.Location):
        return (dest.location_x - cur.location_x) ** 2 + (dest.location_y - cur.location_y) ** 2 <= self.acceptance_radius
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

        if report.status == drone_status.DroneStatus.MOVING and not self.begin_landing:
            if self.at_location(report.position, self.waypoint): 
                command = commands.Command.create_halt_command()
                self.at_waypoint = True
        elif report.status == drone_status.DroneStatus.HALTED or self.begin_landing: 
            if not self.at_waypoint: 
                command = commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x, 
                    self.waypoint.location_y - report.position.location_y
                )
                self.at_waypoint = True 
            else: 
                print("now begin landing!")
                self.begin_landing = True
                res = None
                mn = float('inf')
                for i in landing_pad_locations: 
                    dx = i.location_x - report.position.location_x
                    dy = i.location_y - report.position.location_y
                    dist = dx ** 2 + dy ** 2
                    if dist < mn: 
                        mn = dist
                        res = i
                if res is not None: 
                    if self.at_location(report.position, res): 
                        command = commands.Command.create_land_command();
                    else: 
                        command = commands.Command.create_set_relative_destination_command(
                            res.location_x - report.position.location_x, 
                            res.location_y - report.position.location_y
                        )
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
