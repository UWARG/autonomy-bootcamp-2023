"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
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

        self.waypoint_found = False
        self.landing_pad_found = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
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

        try:
            if report.status == drone_status.DroneStatus.HALTED:
                if not self.waypoint_found:
                    # Debugging information
                    #print(f"Drone position: {report.position.location_x}, {
                    #    report.position.location_y}")
                    #print(f"Waypoint location: {self.waypoint.location_x}, {
                    #    self.waypoint.location_y}")

                    # Command to move to the waypoint
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x,
                        self.waypoint.location_y - report.position.location_y
                    )
                    self.waypoint_found = True

                elif not self.landing_pad_found:
                    # Debugging information
                    #print(f"Landing pads: {landing_pad_locations}")

                    # Find and move to the closest landing pad
                    closest_pad = min(
                        landing_pad_locations, key=lambda pad: self.distance(report.position, pad))
                    print(f"Closest landing pad location: {
                        closest_pad.location_x}, {closest_pad.location_y}")

                    command = commands.Command.create_set_relative_destination_command(
                        closest_pad.location_x - report.position.location_x,
                        closest_pad.location_y - report.position.location_y
                    )
                    self.landing_pad_found = True

                else:
                    # Command to land the drone
                    print("Landing drone.")
                    command = commands.Command.create_land_command()

        except Exception as e:
            print(f"Error in run method: {e}")
            # Optionally, return a null command or handle the error in a way that prevents crashing
            command = commands.Command.create_null_command()

        return command

    def distance(self, l1: location.Location, l2: location.Location):
        return (l1.location_x - l2.location_x)**2 + (l1.location_y - l2.location_y)**2

    # Remove this when done
    # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        #return command
