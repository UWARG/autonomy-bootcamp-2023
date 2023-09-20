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
        self.has_sent_destination = False
        self.has_sent_landing_command = False


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
            print("Halted at: " + str(report.position))
            command=commands.Command.create_set_relative_destination_command(self.waypoint.location_x-report.position.location_x, self.waypoint.location_y-report.position.location_y)
            print("command sent")
            self.command_index += 1

        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_destination:
            pad_to_land=get_closest_pad(self.waypoint, landing_pad_locations)
            command=commands.Command.create_set_relative_destination_command(pad_to_land.location_x-report.position.location_x, pad_to_land.location_y-report.position.location_y)
            self.command_index += 1
            self.has_sent_destination = True

        elif report.status == drone_status.DroneStatus.HALTED and self.has_sent_destination and not self.has_sent_landing_command:
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

def get_closest_pad(waypoint: location.Location, landing_pad_locations: "list[location.Location]")->location.Location:
    print(landing_pad_locations)
    pad_to_land=landing_pad_locations[0]
    min = (landing_pad_locations[0].location_x-waypoint.location_x)**2+(landing_pad_locations[0].location_y-waypoint.location_x)**2
    print("number of landing pads: "+str(len(landing_pad_locations)))
    for landing_pad in landing_pad_locations[1:]:
        distance_temp= (landing_pad.location_x-waypoint.location_x)**2+(landing_pad.location_y-waypoint.location_x)**2
        if  distance_temp < min: 
            min=distance_temp
            pad_to_land=landing_pad
    print("closest: "+str(pad_to_land))
    return pad_to_land
