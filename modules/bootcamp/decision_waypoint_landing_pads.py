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

        self.visited_waypoint = False
        self.acceptance_radius_squared = self.acceptance_radius ** 2
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
        status = report.status
        position = report.position

        if self.visited_waypoint: # Travel to nearest landing pad
            if status == drone_status.DroneStatus.HALTED: # If halted, need to first calculate the nearest landing pad
                self.nearest_landing_pad = self.get_nearest_landing_pad(position, landing_pad_locations)

                if (self.get_relative_location_distance(position, self.nearest_landing_pad) 
                    < self.acceptance_radius_squared):
                    command = commands.Command.create_land_command()
                else:
                    landing_pad_x_dist = self.nearest_landing_pad.location_x - position.location_x
                    landing_pad_y_dist = self.nearest_landing_pad.location_y - position.location_y
                    command = commands.Command.create_set_relative_destination_command(
                        landing_pad_x_dist,
                        landing_pad_y_dist,
                    )
            elif status == drone_status.DroneStatus.MOVING:
                if (self.get_relative_location_distance(position, self.nearest_landing_pad) 
                    < self.acceptance_radius_squared):
                    command = commands.Command.create_halt_command()
        else: # Travel to waypoint
            if status == drone_status.DroneStatus.HALTED:
                if (self.get_relative_location_distance(position, self.waypoint) 
                    > self.acceptance_radius_squared):
                    waypoint_x_dist = self.waypoint.location_x - position.location_x
                    waypoint_y_dist = self.waypoint.location_y - position.location_y
                    command = commands.Command.create_set_relative_destination_command(
                        waypoint_x_dist,
                        waypoint_y_dist,
                    )
                else:
                    self.visited_waypoint = True
            elif status == drone_status.DroneStatus.MOVING:
                if (self.get_relative_location_distance(position, self.waypoint) 
                    < self.acceptance_radius_squared):
                    command = commands.Command.create_halt_command()



            
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    def get_nearest_landing_pad(
            self, 
            position: location.Location, 
            landing_pad_locations: "list[location.Location]",
            ) -> location.Location:
        nearest_landing_pad = None
        nearest_landing_pad_distance = float("inf")
        for landing_pad in landing_pad_locations:
            current_distance = self.get_relative_location_distance(position, landing_pad)
            if current_distance < nearest_landing_pad_distance:
                nearest_landing_pad = landing_pad
                nearest_landing_pad_distance = current_distance
        return nearest_landing_pad
    
    def get_relative_location_distance(
            self, 
            locOne: location.Location, 
            locTwo: location.Location,
            ) -> float:
        return (locOne.location_x - locTwo.location_x) ** 2 + (locOne.location_y - locTwo.location_y) ** 2