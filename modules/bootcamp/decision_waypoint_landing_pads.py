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

        self.reached_waypoint = False
        self.landing_pad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:

        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        if report.status == drone_status.DroneStatus.HALTED:
            # Getting distance to waypoint
            x_diff = self.waypoint.location_x - report.position.location_x
            y_diff = self.waypoint.location_y - report.position.location_y
            squared_distance_to_waypoint = (x_diff ** 2 + y_diff ** 2)

            # Waypoint not reached
            if not self.reached_waypoint:
                # Reached waypoint (within acceptance radius)
                if squared_distance_to_waypoint <= self.acceptance_radius ** 2:
                    self.reached_waypoint = True

                    # Finding closest landing pad
                    squared_smallest_pad_distance = float('inf')
                    for pad in landing_pad_locations:
                        # Getting distance to landing pad
                        pad_x_diff = pad.location_x - report.position.location_x
                        pad_y_diff = pad.location_y - report.position.location_y
                        squared_pad_distance = (pad_x_diff ** 2 + pad_y_diff ** 2) 

                        # Comparing to closest landing pad so far
                        if squared_pad_distance < squared_smallest_pad_distance:
                            squared_smallest_pad_distance = squared_pad_distance
                            self.landing_pad = pad

                    x_diff = self.landing_pad.location_x - report.position.location_x
                    y_diff = self.landing_pad.location_y - report.position.location_y
                    command = commands.Command.create_set_relative_destination_command(x_diff, y_diff)
                
                # Has not reached waypoint yet
                else:
                    command = commands.Command.create_set_relative_destination_command(x_diff, y_diff)

            # Waypoint reached, moving to landing pad
            else:
                # Distance to landing pad
                x_diff = self.landing_pad.location_x - report.position.location_x
                y_diff = self.landing_pad.location_y - report.position.location_y
                squared_distance_to_landing_pad = (x_diff ** 2 + y_diff ** 2)

                if squared_distance_to_landing_pad <= self.acceptance_radius ** 2:
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_set_relative_destination_command(x_diff, y_diff)

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
