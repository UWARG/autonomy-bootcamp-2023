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

        # Add your own
        self.distance = 0
        self.reached_destination = False
        self.closest_distance = float("inf")
        self.index = 0
        self.location = {
            "reached_destination": False,
            "at_pad": False,
            "at_origin": True,
        }
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

        # find the distance from the way point to the
        def distance() -> int:
            size = len(landing_pad_locations)
            for i in range(size):
                pad_x = landing_pad_locations[i].location_x
                pad_y = landing_pad_locations[i].location_y

                nearest_pad_x = self.waypoint.location_x - pad_x
                nearest_pad_y = self.waypoint.location_y - pad_y
                pad_distance = nearest_pad_x**2 + nearest_pad_y**2

                if pad_distance < self.closest_distance**2:
                    self.index = i
                    self.closest_distance = pad_distance

            return self.index

        # Do something based on the report and the state of this class...

        def distance_from_location() -> int:

            # check at which point of the process drone is in and calculate distance accodringly
            if not self.location["reached_destination"]:
                distance_destination = self.waypoint
            else:
                distance_destination = landing_pad_locations[self.index]
            distance_x = report.position.location_x - distance_destination.location_x
            distance_y = report.position.location_y - distance_destination.location_y
            distance_calculate = (distance_x) ** 2 + (distance_y) ** 2

            return distance_calculate

        self.distance = distance_from_location()

        # check if drone is at origin and move drone
        if self.location["at_origin"]:
            self.location["at_origin"] = False
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x, self.waypoint.location_y
            )

        # check if the drone is at the pad and halt drone
        elif (
            self.distance < (self.acceptance_radius**2)
            and not self.location["at_pad"]
        ):
            command = commands.Command.create_halt_command()
            if (self.location["reached_destination"]):
                self.location["at_pad"] = True
            elif(not self.location["reached_destination"]):
                self.location["reached_destination"] = True
                
        # check if drone is at way point and move to pad
        elif self.location["reached_destination"] and not self.location["at_pad"]:
            self.index = distance()
            command = commands.Command.create_set_relative_destination_command(
                landing_pad_locations[self.index].location_x - report.position.location_x,
                landing_pad_locations[self.index].location_y - report.position.location_y,
            )

        # land the drone
        elif self.location["at_pad"] and self.location["reached_destination"]:
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
