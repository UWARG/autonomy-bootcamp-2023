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
        self.state = {
            "reached_waypoint": False,
            "reached_landing_pad": False,
            "got_closest_landing_pad": False,
            "closest_landing_pad_x": 0,
            "closest_landing_pad_y": 0,
            "distance_x": 0,
            "distance_y": 0,
            "relative_distance": 0
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

        # Do something based on the report and the state of this class...
        position = report.position


        def get_closest_landing_pad() -> location.Location:
            """
            Returns the location of the closest landing pad.
            """
            closest_distance = float("inf")
            closest_landing_pad = None
            for landing_pad in landing_pad_locations:
                distance_x = landing_pad.location_x - self.waypoint.location_x
                distance_y = landing_pad.location_y - self.waypoint.location_y
                relative_distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
                if relative_distance < closest_distance:
                    closest_landing_pad = landing_pad

            return closest_landing_pad

        if not self.state["got_closest_landing_pad"]:
            closest_landing_pad = get_closest_landing_pad()
            self.state["closest_landing_pad_x"] = closest_landing_pad.location_x
            self.state["closest_landing_pad_y"] = closest_landing_pad.location_y
            self.state["got_closest_landing_pad"] = True

        if not self.state["reached_waypoint"]:
            self.state["distance_x"] = self.waypoint.location_x - position.location_x
            self.state["distance_y"] = self.waypoint.location_y - position.location_y
        else:
            self.state["distance_x"] = self.state["closest_landing_pad_x"] - position.location_x
            self.state["distance_y"] = self.state["closest_landing_pad_y"] - position.location_y

        self.state["relative_distance"] = (
            (self.state["distance_x"] ** 2 + self.state["distance_y"] ** 2) ** 0.5
        )

        if (self.state["relative_distance"] < self.acceptance_radius
            and not self.state["reached_waypoint"]
        ):
            self.state["reached_waypoint"] = True
        elif (self.state["relative_distance"] < self.acceptance_radius
            and not self.state["reached_landing_pad"]
        ):
            self.state["reached_landing_pad"] = True

        if report.status == drone_status.DroneStatus.HALTED:
            if self.state["reached_landing_pad"]:
                command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(
                    relative_x=self.state["distance_x"],
                    relative_y=self.state["distance_y"]
                )

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
