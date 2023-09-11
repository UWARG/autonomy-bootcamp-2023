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

        self.command_index = 0
        # self.commands = [
        #     commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y),
        # ]

        self.has_sent_landing_command = False

        self.counter = 0

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

        if report.status == drone_status.DroneStatus.HALTED and self.command_index == 0:
            # Print some information for debugging
            print(self.counter)
            # print(self.command_index)
            print("Halted at: " + str(report.position))

            command=commands.Command.create_set_relative_destination_command(self.waypoint.location_x-report.position.location_x, self.waypoint.location_y-report.position.location_y)

            # command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            pad_to_land=get_closest_pad(self.waypoint.location_x, self.waypoint.location_y, landing_pad_locations)
            # command = commands.Command.create_land_command()
            command=commands.Command.create_set_relative_destination_command(landing_pad_locations[pad_to_land].location_x, landing_pad_locations[pad_to_land].location_y)
            self.command_index == 0
            # self.has_sent_landing_command = True

        self.counter += 1


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

def get_closest_pad(self, x: float, y: float, landing_pad_locations: "list[location.Location]")->int:
    pad_to_land=0
    min = ((landing_pad_locations[0].location_x-x)<<2+(landing_pad_locations[1].location_y-y)<<2)>>2
    for i in 1, len(landing_pad_locations):
        distance_temp= ((landing_pad_locations[i].location_x-x)<<2+(landing_pad_locations[i].location_y-y)<<2)>>2
        if  distance_temp < min: 
            min=distance_temp
            pad_to_land=i

    return i