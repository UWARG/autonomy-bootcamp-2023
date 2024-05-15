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
        self.commands = [
            commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y),
        ]

        self.has_sent_landing_command = False
        self.has_arrived_at_waypoint = False

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

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...
        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(self.commands):
            # Print some information for debugging
            print(self.counter)
            print(self.command_index)
            print("Halted at: " + str(report.position))

            command = self.commands[self.command_index]
            # take self position into account
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, self.waypoint.location_y - report.position.location_y)
            self.has_arrived_at_waypoint = True
            self.command_index += 1
        
        elif report.status == drone_status.DroneStatus.HALTED and self.has_sent_landing_command:

            command = commands.Command.create_land_command()

        elif report.status == drone_status.DroneStatus.HALTED and self.has_arrived_at_waypoint:
            nearest_landing_pad = None
            nearest_distance = None

            for landing_pad in landing_pad_locations:
                distance = ((report.position.location_x - landing_pad.location_x) ** 2 + (report.position.location_y - landing_pad.location_y) ** 2)
                if nearest_distance is None or distance < nearest_distance:
                    nearest_distance = distance
                    nearest_landing_pad = landing_pad
            # reduced the number of square root operations to one
            nearest_distance = nearest_distance ** 0.5
            x_dest = nearest_landing_pad.location_x - report.position.location_x
            y_dest = nearest_landing_pad.location_y - report.position.location_y
            # print(x_dest, y_dest)
            command = commands.Command.create_set_relative_destination_command(x_dest, y_dest)
            self.has_sent_landing_command = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        
        return command
