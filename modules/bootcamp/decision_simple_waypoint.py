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

        # Track if the drone is at home or not
        # Starts at home so default is True
        self.at_home = True

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


        # If the drone is at home and halted, set the relative distance to the destination
        if report.status == drone_status.DroneStatus.HALTED and self.at_home == True:
            command = \
                commands.Command.create_set_relative_destination_command(
                    self.waypoint.location_x - report.position.location_x, 
                    self.waypoint.location_y - report.position.location_y
                    )

            self.at_home = False

        # Since the drone is not at home and halted, it is at the destination
        # Drone should land at the destination
        elif report.status == drone_status.DroneStatus.HALTED and self.at_home == False:

            # Handling the random stop problem 
            # Checking if the current coordinates match with the destination
            if report.position.location_x == self.waypoint.location_x and \
                report.position.location_y == self.waypoint.location_y:

                command = commands.Command.create_land_command()

            else:
                command = \
                    commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x, 
                        self.waypoint.location_y - report.position.location_y
                        )



        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
