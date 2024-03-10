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

        self.closest_landing_pad = None
        self.reached_waypoint = False
        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def l2_norm(self, current_loc: location.Location, target_loc: location.Location):
        return (current_loc.location_x - target_loc.location_x)**2 + (current_loc.location_y - target_loc.location_y)**2

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

        if report.status == drone_status.DroneStatus.HALTED:
            # First check if drone is halted.

            if not self.reached_waypoint:
                # If we have not reached waypoint, either set the drone to go to to it
                # or if we have, then find the closest landing pad

                distance_squared = self.l2_norm(report.position, self.waypoint)

                if distance_squared < self.acceptance_radius**2:
                    # Reached waypoint, find closest landing pad and direct the drone to it.

                    self.reached_waypoint = True

                    closest_pad_distance = float('inf')
                    closest_landing_pad = None
                    for lpad in landing_pad_locations:
                        calculated_distance = self.l2_norm(report.position, lpad)
                        if calculated_distance < closest_pad_distance:
                            closest_pad_distance = calculated_distance
                            closest_landing_pad = lpad

                    self.closest_landing_pad = closest_landing_pad

                    if self.closest_landing_pad:
                        # If closest landing pad has been found. 
                        command = commands.Command.create_set_relative_destination_command(
                            self.closest_landing_pad.location_x - report.position.location_x, 
                            self.closest_landing_pad.location_y - report.position.location_y
                        )

                else:
                    # Set the drone to go to the waypoint.
                    command = commands.Command.create_set_relative_destination_command(
                        self.waypoint.location_x - report.position.location_x, 
                        self.waypoint.location_y - report.position.location_y
                    )
            else:
                # Halted at landing pad. Check for distance and land.
                distance_to_pad = self.l2_norm(report.position, self.closest_landing_pad)

                if distance_to_pad < self.acceptance_radius**2:
                    command = commands.Command.create_land_command()






        # if not self.reached_waypoint:
        #     # If we haven't reached waypoint go to it.
        #     distance_squared = self.l2_norm(report.position, self.waypoint)

        #     if report.status == drone_status.DroneStatus.HALTED:
        #         if distance_squared < self.acceptance_radius**2:
        #             self.reached_waypoint = True
        #         else:
        #             command = commands.Command.create_set_relative_destination_command(
        #                 self.waypoint.location_x - report.position.location_x, 
        #                 self.waypoint.location_y - report.position.location_y
        #             )
        # else:
        #     # Waypoint was reached. 
        
        #     if self.closest_landing_pad == None:
        #         # If closest landing pad was not calculated, then find it and go to it.
        #         closest_pad_distance = float('inf')
        #         closest_landing_pad = None
        #         for lpad in landing_pad_locations:
        #             calculated_distance = self.l2_norm(report.position, lpad)
        #             if calculated_distance < closest_pad_distance:
        #                 closest_pad_distance = calculated_distance
        #                 closest_landing_pad = lpad

        #         self.closest_landing_pad = closest_landing_pad

        #     elif report.status == drone_status.DroneStatus.HALTED:
        #         # Closest landing pad has been found. Land.

        #         distance_to_pad = self.l2_norm(report.position, self.closest_landing_pad)

        #         if report.status == drone_status.DroneStatus.HALTED:
        #             if distance_to_pad < self.acceptance_radius**2:
        #                 command = commands.Command.create_land_command()
        #             else:
        #                 command = commands.Command.create_set_relative_destination_command(
        #                     self.closest_landing_pad.location_x - report.position.location_x, 
        #                     self.closest_landing_pad.location_y - report.position.location_y
        #                 )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
