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

        self.plan = ["waypoint", "landing_pad"]
        self.past_waypoints = []

    def square_dist(self, p1: location.Location, p2: location.Location):
        return (p1.location_x - p2.location_x)**2 + (p1.location_y - p2.location_y)**2

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

        if (report.status == drone_status.DroneStatus.HALTED):

            # if list of commands is not finished
            if (len(self.plan) >= 1):

                # if within distance of waypoint
                if (self.square_dist(report.position, self.waypoint) < self.acceptance_radius**2):
                    action = self.plan.pop(0)

                    # redefine waypoint
                    if (action == "landing_pad"):
                        self.past_waypoints.append(self.waypoint)

                        # if no landing pads are nearby, return to starting pad
                        if (len(landing_pad_locations) > 0):
                            self.waypoint = min(landing_pad_locations, key=lambda location : self.square_dist(location, report.position))
                        else:
                            self.waypoint = self.past_waypoints[0]

                x = self.waypoint.location_x - report.position.location_x
                y = self.waypoint.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(x, y)

            # otherwise land
            else:
                command = commands.Command.create_land_command()

        elif (report.status == drone_status.DroneStatus.MOVING):

            # if within distance of waypoint, halt to determine whether to land
            if (not self.square_dist(report.position, self.waypoint) > self.acceptance_radius**2):
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
