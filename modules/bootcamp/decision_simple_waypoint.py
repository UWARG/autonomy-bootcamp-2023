from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """
   

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        self.has_landed = False
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    # ---- helpers ----
   

    

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.
        """
        # Default command advances the simulator without changing state
        command = commands.Command.create_null_command()
        # Already ended?

        # ============ 
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
                # Calculate distance to waypoint
        dx = self.waypoint.location_x - report.position.location_x
        dy = self.waypoint.location_y - report.position.location_y
        dist = (dx**2 + dy**2) ** 0.5

        if self.has_landed:
            return command

        # Do something based on the report and the state of this class...
        if report.status.name == "LANDED":
            self.has_landed = True
            return command

        if dist > self.acceptance_radius:
            if report.status.name == "HALTED":
                command = commands.Command.create_set_relative_destination_command(dx, dy)
        else:
            if report.status.name == "HALTED":
                command = commands.Command.create_land_command()
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
        return command
