"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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
class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
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
        self.halt_at_init_pos = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Make the drone fly to the waypoint.

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

        # Jiwon: Maybe need to change command depending on state of the class

        # waypoint
        # acceptance radius
        
        if report.status == drone_status.DroneStatus.HALTED and self.halt_at_init_pos:
            self.halt_at_init_pos = False
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
        elif report.status == drone_status.DroneStatus.HALTED and not self.halt_at_init_pos:
            command = commands.Command.create_land_command()
            

            
        '''
        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(self.commands):
            # Print some information for debugging
            print(self.counter)
            print(self.command_index)
            

            command = self.commands[self.command_index]
            self.command_index += 1
        elif report.status == drone_status.DroneStatus.HALTED and not self.has_sent_landing_command:
            command = commands.Command.create_land_command()

            self.has_sent_landing_command = True

        self.counter += 1'''


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
