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
        self.state = 0
        self.destination = self.waypoint

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

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
        if report.status == drone_status.DroneStatus.HALTED:
            if self.state == 0:
                # If the drone is near the current destination then set the next destination to closest landing pad
                if self.distance_between_points(self.destination, report.position) <= self.acceptance_radius:
                    # Calculate the distances of the detected landing pad
                    landing_pad_distances = []
                    for landing_pad_location in landing_pad_locations:
                        distance = self.distance_between_points(landing_pad_location, report.position)
                        landing_pad_distances.append(distance)

                    # Find the landing pad closest to the drone
                    shortest_distance = landing_pad_distances[0]
                    self.destination = landing_pad_locations[0]

                    for i, landing_pad_distance in enumerate(landing_pad_distances[1:]):
                        if landing_pad_distance < shortest_distance:
                            shortest_distance = landing_pad_distance
                            self.destination = landing_pad_locations[i]

                    self.state = 1
                # If the drone is not near the destination the travel to destination
                else:
                    destination_relative_to_drone_x = self.destination.location_x - report.position.location_x
                    destination_relative_to_drone_y = self.destination.location_y - report.position.location_y
                    command = commands.Command.create_set_relative_destination_command(
                        destination_relative_to_drone_x,
                        destination_relative_to_drone_y,
                    )

            if self.state == 1:
                if self.distance_between_points(self.destination, report.position) <= self.acceptance_radius:
                    command = commands.Command.create_land_command()
                else:
                    destination_relative_to_drone_x = self.destination.location_x - report.position.location_x
                    destination_relative_to_drone_y = self.destination.location_y - report.position.location_y
                    command = commands.Command.create_set_relative_destination_command(
                        destination_relative_to_drone_x,
                        destination_relative_to_drone_y,
                    )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    @staticmethod
    def distance_between_points(point_1: location.Location, point_2: location.Location) -> float:
        distance_x = point_1.location_x - point_2.location_x
        distance_y = point_1.location_y - point_2.location_y

        return (distance_x ** 2 + distance_y ** 2) ** 0.5
