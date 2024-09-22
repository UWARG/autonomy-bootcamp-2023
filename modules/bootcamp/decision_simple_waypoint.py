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
        print(str(waypoint.location_x) + ", " + str(waypoint.location_y))

        # modifed: not needed now since can't start off with relative command
        # self.command_index = 0
        # self.command = commands.Command.create_set_relative_destination_command(
        #     waypoint.location_x, waypoint.location_y
        # )

        self.has_sent_landing_command = False

        # self.counter = 0

        self.reached_waypoint = False

    def at_waypoint(self, current_x: float, current_y: float) -> bool:
        """
        checks if the drone has reached the waypoint. Returns boolean
        """
        distance_squared = (self.waypoint.location_x - current_x) ** 2 + (
            self.waypoint.location_y - current_y
        ) ** 2
        return distance_squared <= self.acceptance_radius**2

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

        # if it isn't at the waypoint yet, it hasn't reached; so it moves around till it reaches the waypoint

        self.reached_waypoint = self.at_waypoint(
            report.position.location_x, report.position.location_y
        )

        if report.status == drone_status.DroneStatus.HALTED and self.reached_waypoint:
            command = commands.Command.create_land_command()
            self.has_sent_landing_command = True

        elif report.status == drone_status.DroneStatus.HALTED and not self.reached_waypoint:

            relative_x = self.waypoint.location_x - report.position.location_x
            relative_y = self.waypoint.location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(
                relative_x, relative_y
            )

        return command

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
