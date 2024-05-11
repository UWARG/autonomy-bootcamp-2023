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
        self.commands =[commands.Command.create_set_relative_destination_command(waypoint.location_x, waypoint.location_y),
                        commands.Command.create_land_command()]
        self.travaling = False
        self.at_waypoint = False
        self.go_to_closest_pad = False
        # ============
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    # get the radius. 
    def get_position_radius(self, dron_position: "location.Location") -> float:
        return dron_position.location_x ** 2 + dron_position.location_y ** 2
    
    # get the distance bewteen pad and drone
    def get_distance(self, landing_pad_location: "location.Location", 
                     dron_location: "location.Location" ) -> float:
    
            x = landing_pad_location.location_x - dron_location.location_x
            y = landing_pad_location.location_y - dron_location.location_y
            result = x ** 2 + y ** 2
            return result
    
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

        # Program started and go to the way point
        if self.travaling == False and report.status == drone_status.DroneStatus.HALTED and not self.travaling:
            command = self.commands[0]
            self.travaling = True
        
        #drone is at the waypoint and decide which pad is the closest.
        elif self.go_to_closest_pad == False and self.travaling == True and report.status == drone_status.DroneStatus.HALTED:
            
            # get the closest pad position.
            closest_pad = landing_pad_locations[0]
            min_distance = self.get_distance(closest_pad, report.position)
            for pad in landing_pad_locations:
                distance = self.get_distance(pad, report.position)
                if distance < min_distance:
                    min_distance = distance
                    closest_pad = pad

            position = report.position
            command = commands.Command.create_set_relative_destination_command(closest_pad.location_x - position.location_x, closest_pad.location_y - position.location_y)
            self.go_to_closest_pad = True

        # drone is above the pad.
        elif self.go_to_closest_pad == True and report.status == drone_status.DroneStatus.HALTED:
            command = self.commands[1]
        
        # Remove this when done
        #raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    