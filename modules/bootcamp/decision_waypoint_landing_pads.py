class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designated waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        self.closest_landing_pad = None
        self.has_set_destination = False

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.
        """

        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Helper functions
        def within(location1: location.Location, location2: location.Location) -> bool:
            radius_squared = self.acceptance_radius**2
            return (location1.location_x - location2.location_x) ** 2 + (
                location1.location_y - location2.location_y
            ) ** 2 <= radius_squared

        def euclidean_distance_squared(
            location1: location.Location, location2: location.Location
        ) -> int:
            return (location1.location_x - location2.location_x) ** 2 + (
                location1.location_y - location2.location_y
            ) ** 2

        # Travel to waypoint
        if not self.has_set_destination:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x,
                self.waypoint.location_y - report.position.location_y,
            )
            self.has_set_destination = True

        # Check if arrived at waypoint
        elif report.status == drone_status.DroneStatus.MOVING and within(
            report.position, self.waypoint
        ):
            command = commands.Command.create_halt_command()

        # Find and set the closest landing pad once the drone is at the waypoint
        elif self.closest_landing_pad is None and within(report.position, self.waypoint):
            min_distance = float("inf")
            for pad in landing_pad_locations:
                distance = euclidean_distance_squared(report.position, pad)
                if distance < min_distance:
                    min_distance = distance
                    self.closest_landing_pad = pad
            command = commands.Command.create_set_relative_destination_command(
                self.closest_landing_pad.location_x - report.position.location_x,
                self.closest_landing_pad.location_y - report.position.location_y,
            )

        # Land when close to the nearest landing pad
        elif (
            self.closest_landing_pad is not None
            and report.status == drone_status.DroneStatus.HALTED
            and within(report.position, self.closest_landing_pad)
        ):
            command = commands.Command.create_land_command()

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command
