"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
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
class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        # self.l = []
        # self.landing_count = int(input("Enter how many landing locations you want: "))
        # for x in range(self.landing_count):
        #     self.ix = float(input("Enter the x coordinate for the landing location: "))
        #     self.iy = float(input("Enter the y coordinate for the landing location: "))
        #     self.l.append((self.ix, self.iy))        
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

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
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
       
        pos = report.position
        # Do something based on the report and the state of this class...
        print(report.status)

        if report.status == drone_status.DroneStatus.HALTED and pos == self.waypoint:
            command = commands.Command.create_land_command()

        # if report.status == drone_status.DroneStatus.HALTED and len(self.l) != 0:
        #     command = commands.Command.create_set_relative_destination_command(self.l[-1][0] - pos.location_x, self.l[-1][1] - pos.location_y)

        if pos == location.Location(0.0,0.0):
            print(self.waypoint)
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)

        # if pos == location.Location(self.l[-1][0], self.l[-1][1]):
        #     command = commands.Command.create_halt_command()
        #     self.l.pop() 
        
            
            


        # Remove this when done
        

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
