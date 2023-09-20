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

        def square_dist(p1: location.Location, p2: location.Location):
            return (p1.location_x - p2.location_x)**2 + (p1.location_y - p2.location_y)**2
        
        # account for cases where target exceeds flight boundary   
        def controlled_destination(p1: location.Location, p2: location.Location):
            x = p1.location_x - p2.location_x
            y = p1.location_y - p2.location_y

            if (abs(x) > 60 or abs(y) > 60):
                magnitude = max(x, y)
                x = x / magnitude * 60
                y = y / magnitude * 60
                print(x, y)

            return x, y

        if (report.status == drone_status.DroneStatus.HALTED):

            # if list of commands is not finished
            if (len(self.plan) >= 1):

                # if within distance of waypoint
                if (square_dist(report.position, self.waypoint) < self.acceptance_radius**2):
                    action = self.plan.pop(0)

                    # redefine waypoint
                    if (action == "landing_pad"):
                        self.past_waypoints.append(self.waypoint)

                        # if no landing pads are nearby, return to starting pad
                        if (len(landing_pad_locations) > 0):
                            self.waypoint = min(landing_pad_locations, key=lambda location : square_dist(location, report.position))
                        else:
                            self.waypoint = self.waypoint = self.past_waypoints[0]

                x, y = controlled_destination(self.waypoint, report.position)
                command = commands.Command.create_set_relative_destination_command(x, y)

            # otherwise land
            else:
                command = commands.Command.create_land_command()

        elif (report.status == drone_status.DroneStatus.MOVING):

            # if not within distance of waypoint, continue
            if (square_dist(report.position, self.waypoint) > self.acceptance_radius**2):
                command = commands.Command.create_null_command()

            # otherwise land
            else:
                command = commands.Command.create_halt_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
