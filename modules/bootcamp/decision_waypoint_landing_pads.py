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

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    # helper function that calculates euclidean distance (L-2 norm) 
    def euclidean_dist(self, loc1:location.Location, loc2:location.Location):
        x = loc2.location_x - loc1.location_x
        y = loc2.location_y - loc1.location_y

        return (x**2 + y**2)**0.5 

    # helper function to find closest pad from given location
    def find_closest_landing_pad(self, curr_pos, landing_pad_locations: "list[location.Location]"):
        closest_pad = None
        shortest_dist = float('inf')

        for pad in landing_pad_locations:
            dist = self.euclidean_dist(curr_pos, pad)
            if dist < shortest_dist:
                shortest_dist = dist
                closest_pad = pad 

        return closest_pad



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
        status = report.status
        curr_pos = report.position

        # Calculates distance to waypoint
        dist_to_waypoint = self.euclidean_dist(curr_pos, self.waypoint)

        if status == drone_status.DroneStatus.HALTED:

            if dist_to_waypoint <= self.acceptance_radius:

                #Finds the closest landing pad from its current position
                closest_pad = self.find_closest_landing_pad(curr_pos, landing_pad_locations)

                if self.euclidean_dist(curr_pos, closest_pad) <= self.acceptance_radius:
                    command = commands.Command.create_land_command()
                else:
                    command = commands.Command.create_set_relative_destination_command(closest_pad.location_x - curr_pos.location_x,
                                                                                       closest_pad.location_y - curr_pos.location_y)
            else:
                command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x - curr_pos.location_x,
                                                                                   self.waypoint.location_y - curr_pos.location_y)
        elif status == drone_status.DroneStatus.MOVING:
            if dist_to_waypoint <= self.acceptance_radius:
                command = commands.Command.create_halt_command()

        elif status == drone_status.DroneStatus.LANDED:
            command = commands.Command.create_null_command()

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
