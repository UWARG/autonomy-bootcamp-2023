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
def create_move_command_absolute(position, destination):
    # move to target zone by calculating displacement
    relative_x = destination.location_x - position.location_x
    relative_y = destination.location_y - position.location_y
    command = commands.Command.create_set_relative_destination_command(
        relative_x, relative_y
    )

def calc_dist(a, b):
    return (a.location_x - b.location_x) ** 2 + (a.location_y + b.location_y) ** 2

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

        self.waypoint_reached = False

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

        if report.status == drone_status.DroneStatus.MOVING:
            if calc_dist(report.position, report.destination) < self.acceptance_radius:
                command = commands.Command.create_halt_command()
        elif report.status == drone_status.DroneStatus.HALTED:

            if self.waypoint_reached:
                # We are at landing pad, so land
                return commands.Command.create_land_command()

            # Get to the way point
            # check if it is within the appropriate zone

            if calc_dist(report.position, self.waypoint) < self.acceptance_radius**2:
                # Move to nearest landing pad
                # Calculate nearest landing pad
                nearest_landing_pad_location = None
                nearest_landing_pad_dist = float('inf')

                for landing_pad_location in landing_pad_locations:
                    landing_pad_dist = calc_dist(landing_pad_location, report.position)

                    if landing_pad_dist < nearest_landing_pad_dist:
                        nearest_landing_pad_location = landing_pad_location
                        nearest_landing_pad_dist = landing_pad_dist
                
                #check if we are already on the nearest landing pad
                if nearest_landing_pad_dist < self.acceptance_radius ** 2:
                    #land
                    command = commands.Command.create_land_command()
                else:

                    command = create_move_command_absolute(report.position, nearest_landing_pad_location)
                
                self.waypoint_reached = True

            else:
                command = create_move_command_absolute(report.position, self.waypoint)

        # If drone is already landed, or it is moving and not yet reached the destination, we simply return a null command

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
