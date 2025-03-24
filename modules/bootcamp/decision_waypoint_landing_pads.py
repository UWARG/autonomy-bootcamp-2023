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

        # Flag to track if we've reached the waypoint
        self.waypoint_reached = False
        
        # Flag to track if we've chosen a landing pad
        self.landing_pad_selected = False
        
        # Store the chosen landing pad location
        self.target_landing_pad = None
        
        # Flag to track if we've initiated landing
        self.landing_initiated = False
        
        # Flag to track if we've moved (to distinguish initial halt from waypoint halt)
        self.has_moved = False

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

        # If landing was already initiated, just continue with null commands
        if self.landing_initiated:
            return commands.Command.create_null_command()
        
        # Get current position and status
        current_pos = report.position
        current_status = report.status
        
        # If we've selected a landing pad, navigate to it
        if self.landing_pad_selected:
            # Calculate distance to landing pad
            dx = self.target_landing_pad.location_x - current_pos.location_x
            dy = self.target_landing_pad.location_y - current_pos.location_y
            distance = (dx**2 + dy**2)**0.5
            
            # If we've arrived at the landing pad
            if distance <= self.acceptance_radius:
                # If halted, land
                if current_status == drone_status.DroneStatus.HALTED:
                    self.landing_initiated = True
                    return commands.Command.create_land_command()
                # If moving, halt first
                elif current_status == drone_status.DroneStatus.MOVING:
                    return commands.Command.create_halt_command()
            
            # If we're not at the landing pad yet and are halted, move toward it
            if current_status == drone_status.DroneStatus.HALTED:
                return commands.Command.create_set_relative_destination_command(dx, dy)
            
            # If still moving toward landing pad, continue
            return commands.Command.create_null_command()
        
        # If we haven't reached the waypoint yet
        if not self.waypoint_reached:
            # Calculate distance to waypoint
            dx = self.waypoint.location_x - current_pos.location_x
            dy = self.waypoint.location_y - current_pos.location_y
            distance = (dx**2 + dy**2)**0.5
            
            # If we've arrived at the waypoint
            if distance <= self.acceptance_radius:
                # Mark that we've reached the waypoint
                self.waypoint_reached = True
                
                # Find the closest landing pad
                closest_pad = None
                min_distance = float('inf')
                
                for pad in landing_pad_locations:
                    pad_dx = pad.location_x - current_pos.location_x
                    pad_dy = pad.location_y - current_pos.location_y
                    pad_distance = (pad_dx**2 + pad_dy**2)**0.5
                    
                    if pad_distance < min_distance:
                        min_distance = pad_distance
                        closest_pad = pad
                
                # Set the target landing pad
                self.target_landing_pad = closest_pad
                self.landing_pad_selected = True
                
                # If we're moving, halt so we can then move to the landing pad
                if current_status == drone_status.DroneStatus.MOVING:
                    return commands.Command.create_halt_command()
                
                # If already halted, we'll move to landing pad on next iteration
                return commands.Command.create_null_command()
            
            # If we're not at the waypoint yet and halted, move toward it
            if current_status == drone_status.DroneStatus.HALTED:
                self.has_moved = True
                return commands.Command.create_set_relative_destination_command(dx, dy)
        
        # Default: if we're moving and not at waypoint yet, continue
        return commands.Command.create_null_command()
        
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
