"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision


# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        self.waypoint_reached = False

        self.has_sent_landing_command = False

        self.landing_pad_reached = False

        self.counter = 0

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    @staticmethod
    def is_close(x, y, target_x, target_y, tolerance):
        return  abs(x - target_x) < tolerance and abs(y - target_y) < tolerance

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
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
        print("waypoint reached", self.waypoint_reached)
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        

        # Do something based on the report and the state of this class..
        if (
            report.status == drone_status.DroneStatus.HALTED
            and not self.waypoint_reached
            and not self.landing_pad_reached
        ):
            
            print(f"Halted at: {report.position}")
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x-report.position.location_x, 
                self.waypoint.location_y-report.position.location_y
            )
            if self.is_close(report.position.location_x, report.position.location_y, self.waypoint.location_x, self.waypoint.location_y, self.acceptance_radius): 
                self.waypoint_reached = True

        elif report.status == drone_status.DroneStatus.HALTED and self.waypoint_reached:
            # self.waypoint_reached = True
                
            dist = float("inf")
            index = -1
            for i, landing_pad in enumerate(landing_pad_locations):
                ## put this in a helper method
                temp = pow((landing_pad.location_x - report.position.location_x), 2) + pow(
                    (landing_pad.location_y - report.position.location_y), 2
                )

                if temp < dist:
                    dist = temp
                    index = i

            print(landing_pad_locations)
            print("TARGET INDEX:", index)

            command = commands.Command.create_set_relative_destination_command(
                    landing_pad_locations[index].location_x - report.position.location_x,
                    landing_pad_locations[index].location_y - report.position.location_y,
            )
            # print("HALTED AND WAYPOINT REACHED\n\n\n\n\n\n\n\n")

            if not self.landing_pad_reached:
                if index != -1 and (self.is_close(report.position.location_x, report.position.location_y, landing_pad_locations[index].location_x, landing_pad_locations[index].location_y, self.acceptance_radius)):
                    command = commands.Command.create_land_command()
                    self.landing_pad_reached = True
                    self.has_sent_landing_command = True


        self.counter += 1

        print(command)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
