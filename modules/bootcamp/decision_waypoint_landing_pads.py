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
        self.visited = False
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
        
                           
    
            
            
            
        # Default command
       
        command = commands.Command.create_null_command()
       
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        def binomial(a, b, c):
            discr = b**2 - 4*a*c
            ans1 = (-b + discr**(0.5)) / (2*a)
            ans2 = (-b - discr**(0.5)) / (2*a)
            if ans1 > ans2:
                return ((ans2, ans1))
            else:
                return ((ans1, ans2))

        def circle(center_x, center_y, radius, slope, origin):
            squared_term = slope**2 + 1
            x_term = center_x * 2 + slope * (origin + center_y) * 2
            constant = (origin + center_y)**2 + center_x**2 - radius**2
            return binomial(squared_term, x_term, constant)

        def range_check(point_x, point_y, current_x, current_y, radius):
            slope = (current_y - point_y) / (current_x - current_y)
            origin = point_y - point_x * slope


            

            x_points = circle(point_x, point_y, radius, slope, origin)

            y_point1 = slope * x_points[0] + origin
            y_point2 = slope * x_points[1] + origin
            if y_point1 < y_point2:
                y_points = (y_point1, y_point2)
            else:
                y_points = (y_point2, y_point1)
            if current_x >= x_points[0] and current_y >= y_points[0] and current_x <= x_points[1] and current_y <= y_points[1]:
                return True
            else: 
                return False
            
            
            

        def distance_calculator(startx, starty, finalx, finaly):
            return ((finalx-startx)**2 + (finaly-starty)**2)**(1/2)

        def find_min(l, startx, starty):
            mins = -1
            i = None
            for x in range(len(l.copy())):
                dis = distance_calculator(startx, starty, l[x].location_x, l[x].location_y)
                if mins < 0:
                    mins = dis
                    i = x
                elif dis < mins:
                    mins = dis
            return i

        pos = report.position
        close = int(find_min(landing_pad_locations, pos.location_x, pos.location_y))
        if report.status == drone_status.DroneStatus.LANDED and (not range_check(landing_pad_locations[close].location_x, landing_pad_locations[close].location_y, pos.location_x, pos.location_y, self.acceptance_radius)):
            print(self.waypoint)
            command = commands.Command.create_set_relative_destination_command(self.waypoint.location_x, self.waypoint.location_y)
        if self.visited == True and report.status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_land_command()
        if report.status == drone_status.DroneStatus.HALTED and range_check(self.waypoint.location_x, self.waypoint.location_y, pos.location_x, pos.location_y, self.acceptance_radius):
            self.visited = True
            command = commands.Command.create_set_relative_destination_command(landing_pad_locations[close].location_x - pos.location_x, landing_pad_locations[close].location_y - pos.location_y)
            
       

        
        
            
            


        
        

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
