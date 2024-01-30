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
        
        # self.l = []
        # self.landing_count = int(input("Enter how many landing locations you want: "))
        # for x in range(self.landing_count):
        #     self.ix = float(input("Enter the x coordinate for the landing location: "))
        #     self.iy = float(input("Enter the y coordinate for the landing location: "))
        #     self.l.append((self.ix, self.iy))
        # print(self.l)
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        

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
        def distance_calculator(startx, starty, finalx, finaly):
            return ((finalx-startx)**2 + (finaly-starty)**2)**(1/2)

        def find_min(l, mins, startx, starty, i):
            if len(l) == 0:
                return i
            elif mins < 0:
                dis = distance_calculator(startx, starty, l[-1].location_x, l[-1].location_y)
                i = len(l) - 1
                l.pop()
                return find_min(l, abs(dis), startx, starty, i)
            dis = distance_calculator(startx, starty, l[-1].location_x, l[-1].location_y)
            if dis < mins:
                i = len(l) - 1
                l.pop()
                return find_min(l, dis, startx, starty, i)
            l.pop()
            return find_min(l, mins, startx, starty, i)
        # Default command
       
        command = commands.Command.create_null_command()
       
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        
        pos = report.position
        # Do something based on the report and the state of this class...
        print(report.status)
        
        

        # if report.status == drone_status.DroneStatus.HALTED and len(self.l) != 0:
        #     command = commands.Command.create_set_relative_destination_command(self.l[-1][0] - pos.location_x, self.l[-1][1] - pos.location_y)

        if pos == location.Location(0.0,0.0):
            print(self.waypoint)
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
        if report.status == drone_status.DroneStatus.HALTED and pos == self.waypoint:
            close = int(find_min(landing_pad_locations, -1, pos.location_x, pos.location_y, None))
            
            #sclose = 0
            print("HELLO", close)
            print(type(close))
            command = commands.Command.create_set_relative_destination_command(landing_pad_locations[close].location_x - pos.location_x, landing_pad_locations[close].location_y - pos.location_y)
            
        # if pos == landing_pad_locations[0] and self.visited == True:
        #     command = commands.Command.create_land_command()


        # if pos == location.Location(self.l[-1][0], self.l[-1][1]):
        #     command = commands.Command.create_halt_command()
        #     self.l.pop() 
        
            
            


        # Remove this when done
        

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
