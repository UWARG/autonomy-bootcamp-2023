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
        print("Accept radius: ", self.acceptance_radius)

        x = waypoint.location_x
        y = waypoint.location_y
        self.command_index = 0
        self.commands = [commands.Command.create_set_relative_destination_command(x, y)]

        self.has_sent_landing_command = False

        self.counter = 0
        self.can_land = False

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


        if report.status == drone_status.DroneStatus.HALTED and self.command_index < len(
            self.commands
        ):
            print(self.counter)
            print(self.command_index)
            print(len(self.commands))
            print(f"Halted at: {report.position}")
            command = self.commands[self.command_index]
            self.command_index += 1
        elif (
            report.status == drone_status.DroneStatus.HALTED
            and pow(
                (report.position.location_x - self.waypoint.location_x) ** 2
                + (report.position.location_y - self.waypoint.location_y) ** 2,
                0.5,
            )
            > self.acceptance_radius
            and not self.can_land
        ):
            print("not inside acceptance radius")
            self.command_index -= 1
        elif (
            report.status == drone_status.DroneStatus.HALTED
            and not self.has_sent_landing_command
            and not self.can_land
        ):
            closest = pow(60**2 + 60**2, 0.5)
            closest_index = 0
            cur_x = report.position.location_x
            cur_y = report.position.location_y
            for i, pad in enumerate(landing_pad_locations):
                pad_x_diff = landing_pad_locations[i].location_x - cur_x
                pad_y_diff = landing_pad_locations[i].location_y - cur_y
                dist = pad
                dist = pad_x_diff * pad_x_diff + pad_y_diff * pad_y_diff
                if dist < closest:
                    closest = dist
                    closest_index = i            
            self.commands.append(
                commands.Command.create_set_relative_destination_command(
                    landing_pad_locations[closest_index].location_x - cur_x,
                    landing_pad_locations[closest_index].location_y - cur_y,
                )
            )
            self.can_land = True
            print("APPEND + FLAG UP")
            print(len(self.commands))
            print(self.command_index)
            print(landing_pad_locations[closest_index].location_x)
            print(landing_pad_locations[closest_index].location_y)
            command = self.commands[self.command_index]
            self.command_index += 1
        elif (
            report.status == drone_status.DroneStatus.HALTED
            and self.can_land
            and not self.has_sent_landing_command
        ):
            command = commands.Command.create_land_command()
            print("LAND")

            self.has_sent_landing_command = True

        self.counter += 1

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
