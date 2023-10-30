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
        #Helper function for determining relative distance to travel
        def inner_function(relative_flight_boundary_x_abs: float, relative_flight_boundary_y_abs: float)-> "tuple[float, float]":
                min = a if a < b else b
                x_distance = report.destination.location_x - report.position.location_x 
                y_distance = report.destination.location_y - report.position.location_y
                
                x_distance = x_distance if abs(x_distance) < abs(relative_flight_boundary_x_abs else )
                
            
       
            return x + y  # Access the 'x' parameter from the outer function

        default_null_command = commands.Command.create_null_command()
        halt_command = commands.Command.create_halt_command()
        land_command = commands.Command.create_land_command()

        if report.status == drone_status.DroneStatus.MOVING:
            if report.position == report.destination:
                return halt_command
            else:
                return default_null_command

        if report.status == drone_status.DroneStatus.HALTED:
            if report.position == report.destination:
                return land_command
            else:

                
                set_relative_destination_command = (
                    commands.Command.create_set_relative_destination_command(
                        x_distance,
                        y_distance,
                    )
                )
                return set_relative_destination_command

        if report.status == drone_status.DroneStatus.LANDED:
            return default_null_command

        # Detection: Detects landing pad on camera image.

        # Geolocation: Converts bounding boxes to locations.

        # Display: Displays the camera image and drone information.

        #   DroneReport
        #       -  status
        #       -  destination
        #       -  position

        # Remove this when done
        # raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
