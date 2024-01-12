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
        self.command_index = 0
        self.commands = [commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)]
        self.has_sent_landing_command = False
        self.landing = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============   
    def run(self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]") -> commands.Command:
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

        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(self.commands):
            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.landing:
            self.landing = True
            # If on a landing pad already, skip the landing process. Otherwise calculate and set course
            if self.waypoint not in landing_pad_locations:
                landing_pad = self.calculate_closest_pad(report.position, landing_pad_locations)
                command = commands.Command.create_set_relative_destination_command(landing_pad.location_x - report.position.location_x, landing_pad.location_y - report.position.location_y)
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    # -=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==--=-=-=-=-=-=-=-=-=-=-=-
    # HELPER FUNCTIONS
    #  Calculate distance given two locations
    def calculate_distance(self, l1: location.Location, l2: location.Location) -> float:
        return (l2.location_x - l1.location_x)*(l2.location_x - l1.location_x) + (l2.location_y - l1.location_y)*(l2.location_y - l1.location_y)

    # Calculate closest landing pand
    def calculate_closest_pad(self, current_location: location.Location, landing_pads: "list[location.Location]") -> location.Location: 
        closest_landing_pad = None
        closest_distance = float('inf')
        # Loop and find closes landing pad
        for pad in landing_pads:
            distance = self.calculate_distance(pad, current_location)
            if distance < closest_distance:
                closest_distance = distance
                closest_landing_pad = pad
                
        return closest_landing_pad
    # -=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==--=-=-=-=-=-=-=-=-=-=-=-

