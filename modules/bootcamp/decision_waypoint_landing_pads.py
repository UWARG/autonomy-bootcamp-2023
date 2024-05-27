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
        
        self.commands = commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y)

        self.has_sent_landing_command = False

        self.destination = False

        self.landed = False

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
        if report.status == drone_status.DroneStatus.HALTED and not self.destination and not self.landed:
            x_change = self.waypoint.location_x - report.position.location_x
            y_change = self.waypoint.location_y - report.position.location_y
            final = (pow(x_change, 2) + pow(y_change, 2)) ** 0.5

            if final <= self.acceptance_radius:
                self.destination = True
            
            command = self.commands

        elif report.status == drone_status.DroneStatus.HALTED and self.destination and not self.landed:
            distance = 1000.0
            x_final = 0.0
            y_final = 0.0
            length = len(landing_pad_locations)

            for i in range(length):
                loc = landing_pad_locations.pop()
                x_dist1 = self.waypoint.location_x
                x_dist2 = loc.location_x
                y_dist1 = self.waypoint.location_y
                y_dist2 = loc.location_y

                final_dist = (pow(abs(x_dist2 - x_dist1), 2) + pow(abs(y_dist2 - y_dist1), 2)) ** 0.5

                if final_dist < distance:
                    distance = final_dist
                    x_final = x_dist2
                    y_final = y_dist2
        
            x_pad = x_final - self.waypoint.location_x
            y_pad = y_final - self.waypoint.location_y
            self.landed = True

            command = commands.Command.create_set_relative_destination_command((x_pad), (y_pad))

        elif report.status == drone_status.DroneStatus.HALTED and self.landed:    
            command = commands.Command.create_land_command()

            self.has_sent_landing_command = True
        
        return command        


        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
