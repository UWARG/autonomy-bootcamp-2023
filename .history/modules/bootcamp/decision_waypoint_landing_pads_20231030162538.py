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
        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        
        self.arrived_at_waypoint = False


        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self,
        report: drone_report.DroneReport,
        landing_pad_locations: "list[location.Location]",
    ) -> commands.Command:
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

        # Do something based on the report and the state of this class...

        """
        a function to calculate the relative distance that we need to travel based on the difference between current position and the destination
        
        if the status = moving
                if reached destination
                    return a halt command
            return a null comand
    
        if the status is halted
            the drone might have reached the destination 
            see if there is a new destination
            calculate whether the drone has arrived at the destination
            if yes then 
                return a land command (the simulator will end)
            if not then pass in the new destination
            
        The difference between the coordinates of the drone position and waypoint under the text file in log/ should be less than 0.1
        
        """

        # Helper function for determining relative distance to travel
        def get_set_relative_distance_command(
            starting_location:location.Location, destination_location:location.Location,
            relative_flight_boundary_x_abs: float, relative_flight_boundary_y_abs: float
  
        ) -> commands.Command:
            x_distance = destination_location.location_x - starting_location.location_x
            y_distance = destination_location.location_y - starting_location.location_y
            

            #I put the minus operator at the place ^ for a previous try, it doesn't work since subtracting boolean values is not accepted behavior in python
            try:
                sign_x_distance = (x_distance > 0) ^ (x_distance < 0)
                sign_y_distance = (y_distance > 0) ^ (y_distance < 0)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                
            


            x_distance = (
                x_distance
                if abs(x_distance) < abs(relative_flight_boundary_x_abs)
                else (relative_flight_boundary_x_abs * sign_x_distance)
            )
            y_distance = (
                y_distance
                if abs(y_distance) < abs(relative_flight_boundary_y_abs)
                else (relative_flight_boundary_y_abs * sign_y_distance)
            )
            


            set_relative_destination_command = (
                commands.Command.create_set_relative_destination_command(
                    x_distance,
                    y_distance,
                )
            )
            

            return set_relative_destination_command

        def validate_arrival_at_destination(
            flight_position: location.Location, destination_position: location.Location
        ):
            # print(
            #     "flight_position.location_x,flight_position.location_y",
            #     flight_position.location_x,
            #     flight_position.location_y,
            # )
            # print(
            #     "destination_position.location_x, destination_position.location_y",
            #     destination_position.location_x,
            #     destination_position.location_y,
            # )
            if abs(flight_position.location_x - destination_position.location_x) > 0.1:
                return False
            if abs(flight_position.location_y - destination_position.location_y) > 0.1:
                return False
            return True


        # Loop through the list of landing pad locations and find the nearest landing pad from the original location by finding the minimum L2 norm between the starting position and the landingpad_locations
        def calculate_nearest_landing_pad(
            starting_position: location.Location,
            landingpad_locations: "list[location.Location]",
        ) ->location.Location:
            
            min = 999
            nearest_landingpad = landing_pad_locations[0]
            
            for landingpad_location in landingpad_locations:
                temp = calculate_l2_norm(starting_position, landingpad_location)
                if(temp< min):
                    min = temp
                    nearest_landingpad = landingpad_location
                print(min)
        
            return nearest_landingpad

        def calculate_l2_norm(
            location1: location.Location, location2: location.Location
        ) -> int:
            x_dif = location1.location_x - location2.location_x
            y_dif = location1.location_y - location2.location_y
            
            l2norm = (x_dif**2 + y_dif**2) ** 0.5
            return l2norm

        default_null_command = commands.Command.create_null_command()
        halt_command = commands.Command.create_halt_command()
        land_command = commands.Command.create_land_command()
        
        #print("report destination:",report.destination)

        if self.arrived_at_waypoint == False:
            if report.status == drone_status.DroneStatus.MOVING:
                if validate_arrival_at_destination(report.position, self.waypoint):
                    return halt_command
                else:
                    return default_null_command

            if report.status == drone_status.DroneStatus.HALTED:
                # arrives at the destination
                if validate_arrival_at_destination(report.position, self.waypoint):
                    self.arrived_at_waypoint = True
                    return halt_command
                else:
                    set_relative_destination_command_result = (
                        get_set_relative_distance_command(report.position,self.waypoint,60, 60)
                    )
                    return set_relative_destination_command_result

            if report.status == drone_status.DroneStatus.LANDED:
                return default_null_command
        else:
            #print("Entered stage after arriving at the waypoint---------------------------")
            

            if report.status == drone_status.DroneStatus.HALTED:
                nearest_landing_pad_result = calculate_nearest_landing_pad(report.position,landing_pad_locations)
                
                if validate_arrival_at_destination(report.position, nearest_landing_pad_result):
                    return land_command
                else:
                    set_relative_destination_command_result = (
                        get_set_relative_distance_command(report.position,nearest_landing_pad_result,60, 60)
                    )
                    return set_relative_destination_command_result
                
            if report.status == drone_status.DroneStatus.MOVING:
                
                if validate_arrival_at_destination(report.position, nearest_landing_pad_result):
                    return halt_command
                else: 
                    return default_null_command
                
            if report.status == drone_status.DroneStatus.LANDED:
                return default_null_command
        

        # Detection: Detects landing pad on camera image.

        # Geolocation: Converts bounding boxes to locations.

        # Display: Displays the camera image and drone information.

        #   DroneReport
        #       -  status
        #       -  destination
        #       -  position

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
