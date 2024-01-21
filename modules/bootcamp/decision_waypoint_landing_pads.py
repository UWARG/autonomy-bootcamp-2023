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
        self.is_at_waypoint = False
        self.is_at_closest_waypoint = False

        

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

        def find_shortest_distance(curr_location, landing_pad_locations_list):
            min_distance = float('inf')
            closest_waypoint = landing_pad_locations_list[0]
            for landing_pad in landing_pad_locations_list:
                x = landing_pad.location_x - curr_location.location_x
                y = landing_pad.location_y - curr_location.location_y

                distance = (x ** 2)+(y ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_waypoint = landing_pad

            return closest_waypoint

        if report.status == drone_status.DroneStatus.HALTED and self.is_at_waypoint == False:
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - report.position.location_x, 
                                                                               self. waypoint.location_y - report.position.location_y)
            self.is_at_waypoint = True

        elif report.status == drone_status.DroneStatus.HALTED and self.is_at_closest_waypoint == False:
            closest_location = find_shortest_distance(report.position, landing_pad_locations)
            if closest_location != report.position:
                x = closest_location.location_x - report.position.location_x
                y = closest_location.location_y - report.position.location_y
                command = commands.Command.create_set_relative_destination_command(x, y)
                self.is_at_closest_waypoint = True

        elif report.status == drone_status.DroneStatus.HALTED and self.is_at_closest_waypoint == True:
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
    
    