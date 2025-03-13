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
        self.waypoint_x = waypoint.location_x
        self.waypoint_y = waypoint.location_y

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
        self.drone_x_pos = report.position.location_x
        self.drone_y_pos = report.position.location_y

        # Compute movement toward waypoint
        self.x_difference = self.waypoint_x - self.drone_x_pos
        self.y_difference = self.waypoint_y - self.drone_y_pos

        # Helper function to calculate Euclidean distance using index
        def Euclidean_Dist(i):
            pad = landing_pad_locations[i]
            return ((pad.location_x - self.drone_x_pos) ** 2 + (pad.location_y - self.drone_y_pos) ** 2) ** 0.5

        # Default to moving towards waypoint
        if (self.x_difference**2 + self.y_difference**2)**0.5 > self.acceptance_radius:
            print(f"Moving toward waypoint at ({self.waypoint_x}, {self.waypoint_y})")
            try:
                command = commands.Command.create_set_relative_destination_command((self.x_difference, self.y_difference))
            except Exception as e:
                print("Error sending move command:", e)
                print("Issuing hover command instead.")
                command = commands.Command.create_hover_command()
                
        else:
            print("Waypoint reached! Searching for nearest landing pad...")

            if not landing_pad_locations:
                print("No landing pads detected. Landing at waypoint.")
                return commands.Command.create_land_command()

            # Initialize variables for finding the nearest landing pad
            nearest_pad_index = 0
            nearest_distance = Euclidean_Dist(nearest_pad_index)

            # Find the nearest landing pad using Euclidean distance
            for i in range(1, len(landing_pad_locations)):
                current_distance = Euclidean_Dist(i)
                if current_distance < nearest_distance:
                    nearest_pad_index = i
                    nearest_distance = current_distance

            # Get the nearest landing pad location
            nearest_pad = landing_pad_locations[nearest_pad_index]

            # Calculate the differences toward the landing pad
            pad_x_diff = nearest_pad.location_x - self.drone_x_pos
            pad_y_diff = nearest_pad.location_y - self.drone_y_pos
            pad_distance = (pad_x_diff ** 2 + pad_y_diff ** 2) ** 0.5

            # Move towards the landing pad if not close enough, otherwise land
            if pad_distance > self.acceptance_radius:
                print(f"Moving toward landing pad at ({nearest_pad.location_x}, {nearest_pad.location_y})")
                command = commands.Command.create_set_relative_destination_command((pad_x_diff, pad_y_diff))
            else:
                print(f"Landing at nearest pad at ({nearest_pad.location_x}, {nearest_pad.location_y})")
                command = commands.Command.create_land_command()

        # Do something based on the report and the state of this class...

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
