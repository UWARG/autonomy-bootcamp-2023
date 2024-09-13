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
        #set as closest landing to waypoint
        self.smallestnorm = [float("inf"), float("inf")]
        self.command_index = 0
        self.commands = [
            commands.Command.create_set_relative_destination_command(waypoint.location_x,waypoint.location_y)
        ]

        self.has_sent_landing_command = False
        self.initializing_halt = True
        self.is_halt_at_waypoint = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        
        # Do something based on the report and the state of this class...
        if report.status ==  drone_status.DroneStatus.HALTED:
            print(self.is_halt_at_waypoint)
            if self.initializing_halt:
                command = self.commands[self.command_index]
                self.initializing_halt = False
                self.is_halt_at_waypoint = True
                print("Origin To Waypoint: Success")
                print(self.is_halt_at_waypoint)
                print("CHECK ABOVE")
            elif self.is_halt_at_waypoint == True:
                print("Staring ")
                for landingpad in landing_pad_locations:
                    print(landingpad)
                    if landingpad.location_x**2 + landingpad.location_y**2  < self.smallestnorm[0]**2 + self.smallestnorm[1]**2:
                        print(landingpad)
                        self.smallestnorm[0],self.smallestnorm[1] = (landingpad.location_x, landingpad.location_y)
                command = commands.Command.create_set_relative_destination_command(self.smallestnorm[0]-self.waypoint.location_x,
                                                                                   self.smallestnorm[1]-self.waypoint.location_y)
                #print(landingpad)
                self.is_halt_at_waypoint = False 
            else:
                print(self.is_halt_at_waypoint)
                print("Funnyhaha")
                command = commands.Command.create_land_command()
                self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
