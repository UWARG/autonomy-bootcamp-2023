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
        self.commands = [
            commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)
        ]
        self.landed_at_waypoint = False
        self.has_sent_landing_command = False
        self.landing_pad_cache = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    def getL2Norm(self, l1: location.Location, l2: location.Location) -> int:
        return (l2.location_x - l1.location_x) * (l2.location_x - l1.location_x) + (l2.location_y - l1.location_y) * (l2.location_y - l1.location_y)
    
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

        if report.status == drone_report.drone_status.DroneStatus.HALTED and self.command_index<len(self.commands):
            command = self.commands[self.command_index]
            self.command_index += 1

        elif report.status == drone_report.drone_status.DroneStatus.HALTED and not self.landed_at_waypoint:
            
            self.landed_at_waypoint = True
            min_landing_distance = 10000000
            for landing_pad in landing_pad_locations:
                distance_to_lp = self.getL2Norm(landing_pad, report.position)
                if distance_to_lp < min_landing_distance:
                    self.landing_pad_cache = landing_pad
                    min_landing_distance = distance_to_lp
            
            location_delta_x = self.landing_pad_cache.location_x - report.position.location_x
            location_delta_y = self.landing_pad_cache.location_y - report.position.location_y
            self.commands.append(commands.Command.create_set_relative_destination_command(location_delta_x, location_delta_y))
            command = self.commands[self.command_index]
            
            self.command_index += 1

        elif report.status == drone_report.drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            self.has_sent_landing_command = True
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
