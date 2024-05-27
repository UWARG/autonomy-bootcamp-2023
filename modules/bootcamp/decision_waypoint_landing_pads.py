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
        self.travel_to_pad = False
        self.closest_pad = None
        self.landed = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def get_relative_distance_sqr(self, position: location.Location, 
                                  other: location.Location) -> float:
        """
        Gets the square of the distance between the position of the drone and another location.

        position: the current location of the drone
        other: the location of the object you wish to obtain the distance of

        Return: the distance between the drone and the object
        """
        return (other.location_x - position.location_x) ** 2 + (other.location_y - 
                                                                position.location_y) ** 2

    def find_closest_pad(self, position: location.Location, 
                         landing_pad_locations: "list[location.Location]") -> "location.Location | None":
        """
        Finds the index of the closest landing pad within the list 'landing_pad_locations'.

        position: the current location of the drone
        landing_pad_locations: a list containing the locations of all the landing pads nearby

        Return: the index of the closest landing pad to the drone in the list 
                'landing_pad_locations'
        """
        min_distance_sqr = float("inf")
        closest_pad = None

        for landing_pad_location in landing_pad_locations:
            current_pad_distance = self.get_relative_distance_sqr(position, landing_pad_location)
            if current_pad_distance < min_distance_sqr:
                min_distance_sqr = current_pad_distance
                closest_pad = landing_pad_location

        return closest_pad


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
        if self.landed:
            # If the drone is landed, we don't want to issue anymore commands
            return command

        elif self.travel_to_pad:
            # Once the drone needs to travel to a pad 

            if self.closest_pad is not None and self.get_relative_distance_sqr(report.position, 
                                                                               self.closest_pad) < self.acceptance_radius ** 2 and report.status == drone_status.DroneStatus.MOVING:
                # If we're on the pad and we're still moving, we want to halt the pad
                command = commands.Command.create_halt_command()

            elif self.closest_pad is not None and self.get_relative_distance_sqr(report.position, 
                                                                                 self.closest_pad) < self.acceptance_radius ** 2 and report.status == drone_status.DroneStatus.HALTED:
                # If we're on the pad and halted, now we want to land on the pad
                command = commands.Command.create_land_command()
                self.landed = True

            elif self.closest_pad is not None and report.status == drone_status.DroneStatus.HALTED:
                # Otherwise, we still need to move to the pad
                command = commands.Command.create_set_relative_destination_command(self.closest_pad.location_x - report.position.location_x, 
                                                                                   self.closest_pad.location_y - report.position.location_y)


        elif self.get_relative_distance_sqr(report.position, 
                                            self.waypoint) < self.acceptance_radius and report.status == drone_status.DroneStatus.HALTED:
            # Once we have reached the waypoint, we now want to halt
            command = commands.Command.create_halt_command()
            # After halting, we now want to make the drone fly to the nearest pad on the next command
            self.travel_to_pad = True
            self.closest_pad = self.find_closest_pad(report.position, landing_pad_locations)

        elif report.status == drone_status.DroneStatus.HALTED:
            print(report.position == self.waypoint)
            print(self.travel_to_pad)
            print(f"Halted At: {str(report.position)}")
            difference_x = self.waypoint.location_x - report.position.location_x
            difference_y = self.waypoint.location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(difference_x, difference_y)
            print(f"Moving: ({str(difference_x)}, {str(difference_y)})")

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
