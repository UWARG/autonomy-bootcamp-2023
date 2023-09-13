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
        self.destination = waypoint #preset destination to waypoint so drone has intial direction
        self.has_taken_off = False
        self.change_destination = False
        self.prev_num_landing_pads = 1

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
    def find_nearest_landing_pad(self, waypoint: location.Location, landing_pad_locations: "list[location.Location]") -> int:
        """
        To determine closest landing pad in frame to waypoint and return it's index.
        Index is returned instead of object to improve speed
        """
        
        # setting intial shortest values, to be changed
        shortest_distance = 10000000
        shortest_index = None

        for i, pad in enumerate(landing_pad_locations):
            # use distance formula to find distance between pad and waypoint
            distance = ((waypoint.location_x - pad.location_x)**2 + (waypoint.location_y - pad.location_y)**2)**0.5

            #check if pad is closest to waypoint and update values
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_index = i


        return shortest_index

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
        
        
        #print(self.change_destination, self.has_taken_off, report.status == drone_status.DroneStatus.MOVING)
        
        # actions for once drone has taken off and is flying
        
        if self.has_taken_off:
            
            # update destination to closest landing pad to waypoint
            # only updates closest landing pad once there is a change in the number of landing pads available
            # prevents drone from going back to origin, looking for landing pads when none are visible, and repeatedly searching for new closest when same pads are on screen
            num_landing_pads = len(landing_pad_locations)
            if num_landing_pads > 0 and not self.prev_num_landing_pads == num_landing_pads:
                index = self.find_nearest_landing_pad(self.waypoint, landing_pad_locations)
                self.destination = landing_pad_locations[index]  # update destination to indexed location in list
                command = commands.Command.create_halt_command()
                self.change_destination = True  # sets staus to change destination mode

            # actions once drone has reached destination
            if report.position.__eq__(report.destination):  
                if report.status == drone_status.DroneStatus.MOVING:  # halt if previously moving
                    command = commands.Command.create_halt_command()
                if report.status == drone_status.DroneStatus.HALTED:  # land if previously halted, and prepare status for next takeoff
                    command = commands.Command.create_land_command()
                    self.has_taken_off = False
            
                
        # sets drones initial destination to waypoint and destinations to landing pads as they become visible
        # updates drone flight and direction changing status
        if report.status == drone_status.DroneStatus.HALTED and (not self.has_taken_off or self.change_destination) and not report.position.__eq__(self.destination):
            command = commands.Command.create_set_relative_destination_command(self.destination.location_x - report.position.location_x, self.destination.location_y - report.position.location_y)
            self.has_taken_off = True
            self.change_destination = False

        self.prev_num_landing_pads = len(landing_pad_locations)  # update number of landing pads from the previous frame
    

        # Remove this when done
        #raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
