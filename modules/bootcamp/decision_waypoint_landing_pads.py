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
        self.acceptance_radius = acceptance_radius
        self.distance_y = 0
        self.distance_x = 0
        self.distance = 0
        self.reached_destination = False
        self.nearest_pad_x = 0
        self.nearest_pad_y = 0
        self.pad_distance = 0
        self.closest_distance = float('inf')
        self.index = 0
        self.at_pad = False
        self.at_origin = True
        self.distance_destination = ""
        self.distance_calculate = 0
        self.x =0
        self.y = 0
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

        #find the distance from the way point to the 
        def distance():
            size = len(landing_pad_locations)
            for i in range(size):
                pad_x = landing_pad_locations[i].location_x
                pad_y = landing_pad_locations[i].location_y

                self.nearest_pad_x = self.waypoint.location_x - pad_x
                self.nearest_pad_y = self.waypoint.location_y - pad_y
                self.pad_distance = (self.nearest_pad_x**2 + self.nearest_pad_y**2)**0.5

                if(self.pad_distance < self.closest_distance):
                    self.index = i
                    self.closest_distance = self.pad_distance

            return self.index
        

        # Do something based on the report and the state of this class...

        def distance_from_location():
            if self.reached_destination == False:
                self.distance_destination = self.waypoint
            else:
                self.distance_destination = landing_pad_locations[self.index]
            self.distance_x = report.position.location_x - self.distance_destination.location_x
            self.distance_y = report.position.location_y - self.distance_destination.location_y
            self.distance_calculate = ((self.distance_x)**2 + (self.distance_y)**2)**0.5

            return self.distance_calculate
        
        self.distance = distance_from_location()
    

        #check if the drone is at the waypoint
        if(self.at_pad and self.reached_destination):
            command = commands.Command.create_land_command()
        #check if the drone is at the origin
        elif(self.at_origin):
            self.at_origin = False
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
        #check if at the waypoint
        elif(self.distance<self.acceptance_radius and not self.reached_destination and not self.at_pad):
            self.reached_destination = True
            command = commands.Command.create_halt_command()
        elif(self.distance<self.acceptance_radius and self.reached_destination and not self.at_pad):
            self.at_pad =True
            command = commands.Command.create_halt_command()
        #check if drone is at way point and move to pad
        elif(self.reached_destination and not self.at_pad):
            self.index = distance()
            self.x = landing_pad_locations[self.index].location_x - report.position.location_x
            self.y = landing_pad_locations[self.index].location_y - report.position.location_y
            command = commands.Command.create_set_relative_destination_command(self.x, self.y)
        #check if the drone is at the waypoint and halted, move to pad
           
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
