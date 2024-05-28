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
            commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)
        ]

        self.has_sent_landing_command = False
        self.go_to_landing_pad = False

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
        if report.status == drone_status.DroneStatus.HALTED and not self.go_to_landing_pad:
            # Print some information for debugging
            print(self.counter)
            print(self.command_index)
            print("Halted at: " + str(report.position))

            
            command = self.commands[self.command_index]

            self.go_to_landing_pad = True
        elif report.status == drone_status.DroneStatus.HALTED and self.go_to_landing_pad and not self.has_sent_landing_command:
            nearest_landing_pad = landing_pad_locations[0]
            min_distance = ((nearest_landing_pad.location_x - report.position.location_x)**2 + (nearest_landing_pad.location_y - report.position.location_y)**2)**0.5
            print("123456789")
            for landing_pad in landing_pad_locations:
                distance = ((landing_pad.location_x - report.position.location_x)**2 + (landing_pad.location_y - report.position.location_y)**2)**0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_landing_pad = landing_pad
            position = report.position
            command = commands.Command.create_set_relative_destination_command(nearest_landing_pad.location_x - position.location_x, nearest_landing_pad.location_y - position.location_y)

            self.has_sent_landing_command = True
        elif report.status == drone_status.DroneStatus.HALTED and self.has_sent_landing_command:
            command = commands.Command.create_land_command()
            
            

        self.counter += 1

        # Remove this when done

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
