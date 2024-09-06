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
        self.waypoint_reached = False
        self.reached_landing_pad = False
        self.moving_to_landing_pad = False
        self.target_landing_pad = None

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    
    def distance_to_waypoint(self, drone_location: location.Location) -> float:
        """
        Calculate the distance between the drone and the waypoint (unsquare-rooted).
        """
        return self._get_distance(drone_location, self.waypoint)

    def _get_distance(self, drone_location: location.Location, waypoint: location.Location) -> float:
        """
        Calculate the distance between two points (unsquare-rooted).
        """
        return ((drone_location.location_x - waypoint.location_x)**2 + (drone_location.location_y - waypoint.location_y)**2) 

    def distance_to_landing_pad(self, drone_location: location.Location, landing_pad_location: location.Location) -> float:
        """
        Calculate the distance between the drone and the landing pad (unsquare-rooted).
        """
        return self._get_distance(drone_location, landing_pad_location)

    def get_relative_displacement(self, drone_location: location.Location) -> location.Location:
        """
        Calculate the relative displacement between the drone and the waypoint.
        """
        
        return location.Location(self.waypoint.location_x - drone_location.location_x, self.waypoint.location_y - drone_location.location_y)

    def get_displacement_from_landing_pad(self, drone_location: location.Location, landing_pad_location: location.Location) -> location.Location:
        """
        Calculate the relative displacement between the drone and the landing pad.
        """
        return location.Location(landing_pad_location.location_x - drone_location.location_x, landing_pad_location.location_y - drone_location.location_y)

    def get_closest_landing_pad(self, landing_pad_locations: "list[location.Location]") -> location.Location:
        """
        Get the closest landing pad to the drone (from the waypoint).
        """
        # first assume the closest landing pad is the first one
        closest_landing_pad = landing_pad_locations[0]
        closest_distance = self.distance_to_waypoint(closest_landing_pad)
        # now iterate and find the closest one
        for landing_pad in landing_pad_locations:
            distance = self.distance_to_waypoint(landing_pad)
            if distance < closest_distance:
                closest_landing_pad = landing_pad
                closest_distance = distance

        return closest_landing_pad

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
        if report.status == drone_status.DroneStatus.MOVING:
            # if the drone is moving, we don't need to do anything
            return command
        
        if self.reached_landing_pad:
            print("Landing")
            command = commands.Command.create_land_command()
            return command

        # if waypoint is reached, we find closes landing pad and go there
        if self.waypoint_reached and not self.moving_to_landing_pad:
            print("Reached waypoint... Determining landing pad")
            # get closest landing pad
            self.target_landing_pad = self.get_closest_landing_pad(landing_pad_locations)
            print("Closest landing pad: " + str(self.target_landing_pad))
            # relative pos of land pad from current pos
            relative_destination_from_current_position = self.get_displacement_from_landing_pad(report.position, self.target_landing_pad)
            self.moving_to_landing_pad = True
            command = commands.Command.create_set_relative_destination_command(
                relative_destination_from_current_position.location_x,
                relative_destination_from_current_position.location_y
            )

            print("Sending command to move to landing pad")
            return command

        # checks if the drone is within the acceptance radius
        if not self.moving_to_landing_pad and self.distance_to_waypoint(report.position) <= self.acceptance_radius ** 2:
            print("Waypoint reached")
            self.waypoint_reached = True
            command = commands.Command.create_halt_command()
            return command

        # if the drone is moving to the landing pad, check if it has reached it
        if self.moving_to_landing_pad:
            if self.distance_to_landing_pad(report.position, self.target_landing_pad) <= self.acceptance_radius ** 2:
                print("Reached landing pad")
                self.reached_landing_pad = True
                command = commands.Command.create_halt_command()
                return command

        # if not moving and none of the above, we take off
        if report.status == drone_status.DroneStatus.HALTED and not self.waypoint_reached:
            print("Moving to waypoint")

            relative_destination_from_current_position = self.get_relative_displacement(report.position)
            command = commands.Command.create_set_relative_destination_command(
                relative_destination_from_current_position.location_x,
                relative_destination_from_current_position.location_y
            )


            # ============
            # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
            # ============

        return command
