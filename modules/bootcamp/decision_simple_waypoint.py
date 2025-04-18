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

        # Add your own

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

        if report.status == drone_status.DroneStatus.HALTED:
            #Things to check for a halted drone:
            # Does it have a valid destination
            # If no, set destanation and movemenet
            #
            # If yes, 
            #   - Check if in acceptable radius of destination
            #   - If yes, land
            #   - Otherwise, restart movement to destination   
            #
            
            pass
            
        elif report.status == drone_status.DroneStatus.MOVING:
            # Check if drone is proximity of destination
            # IF no,
            # Confirm that the drone is moving in the correct direction: Takes constant time to do

            
            pass
        else:
            # Landed case


        # CHeck if the drone has a valid destination
        # If not, set to waypoint in init command
        # Set global destination to that landing pad cords

        # Create a new function to calculate the direction to the desired location
        # If the drone is already moving to that position, then allow it to continue
        
        # If drone is halted check that it is in the acceptable radius of the waypoint
        # Use euclidian distance to check that it is the case

        # Land once in the correct position
    



        # So we have a report to play around wiht and locations

        # Do something based on the report and the state of this class...

        # valid statuses:
        # - Halted
        # - Moving
        # - Landed

        # - Report contains position and global destination
        # - For halted and landed drones, position and global dest are equal

        # Four actions

        # - Null: default, do nothing
        # - set relative dest: move drone to distance RELATIVE to current pos
        #       - Note: requires drone to be halted to use

        # - Halt: Makes drone stop immediately at current position
        # - Land: Lands drone at current position and ends simulation ( requires drone to be halted)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
