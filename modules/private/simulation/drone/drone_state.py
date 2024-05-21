"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Simple simulation of drone in world.
"""

import math

from . import drone_velocity
from .... import commands
from .... import drone_report
from .... import drone_status
from .... import location


# Basically a struct
# pylint: disable-next=too-many-instance-attributes
class DroneState:
    """
    Contains drone simulation state.
    """

    __create_key = object()

    __MAX_SPEED = 5.0  # m/s
    __MAX_ACCEPTANCE_RADIUS = 1.0

    @classmethod
    def create(
        cls,
        time_step_size: float,
        initial_position: location.Location,
        boundary_bottom_left: location.Location,
        boundary_top_right: location.Location,
        acceptance_radius: float,
    ) -> "tuple[bool, DroneState | None]":
        """
        time_step_size: \\delta t in seconds.
        initial_position: Initial position of drone.
        boundary is xyxy corners of map area.
        acceptance_radius: Distance within destination drone is considered to have arrived.
        """
        if time_step_size <= 0.0:
            return False, None

        if boundary_bottom_left.location_x >= boundary_top_right.location_x:
            return False, None

        if boundary_bottom_left.location_y >= boundary_top_right.location_y:
            return False, None

        if not cls.__is_within_boundary(initial_position, boundary_bottom_left, boundary_top_right):
            return False, None

        if acceptance_radius <= 0.0:
            return False, None

        if acceptance_radius > cls.__MAX_ACCEPTANCE_RADIUS:
            return False, None

        return True, DroneState(
            cls.__create_key,
            time_step_size,
            initial_position,
            boundary_bottom_left,
            boundary_top_right,
            acceptance_radius,
        )

    # Better to be explicit with parameters
    # pylint: disable-next=too-many-arguments
    def __init__(
        self,
        class_private_create_key,
        time_step_size: float,
        initial_position: location.Location,
        boundary_bottom_left: location.Location,
        boundary_top_right: location.Location,
        acceptance_radius: float,
    ):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneState.__create_key, "Use create() method"

        # Map area boundary
        self.__boundary_top_left = boundary_bottom_left
        self.__boundary_bottom_right = boundary_top_right

        # Simulation state
        self.__current_step: int = 0

        # Intent state
        self.__status = drone_status.DroneStatus.HALTED
        self.__destination = initial_position
        self.__acceptance_radius = acceptance_radius
        self.__commands = []  # List of all commands received by the drone

        # Physical state
        self.__time_step_size = time_step_size
        _, velocity = drone_velocity.DroneVelocity.create(0.0, 0.0)
        assert velocity is not None
        self.__velocity: drone_velocity.DroneVelocity = velocity
        self.__position = initial_position

    @staticmethod
    def __is_within_boundary(
        position: location.Location,
        boundary_bottom_left: location.Location,
        boundary_top_right: location.Location,
    ) -> bool:
        """
        Checks whether position is within bounds.
        """
        if (
            position.location_x < boundary_bottom_left.location_x
            or position.location_x > boundary_top_right.location_x
        ):
            return False

        if (
            position.location_y < boundary_bottom_left.location_y
            or position.location_y > boundary_top_right.location_y
        ):
            return False

        return True

    def __update_intent(self, status: drone_status.DroneStatus, destination: location.Location):
        """
        Update intent of drone.
        """
        self.__status = status
        self.__destination = destination

        velocity = None
        if self.__status != drone_status.DroneStatus.MOVING:
            _, velocity = drone_velocity.DroneVelocity.create(0.0, 0.0)
        else:
            relative_x = self.__destination.location_x - self.__position.location_x
            relative_y = self.__destination.location_y - self.__position.location_y
            result, velocity = self.__set_course(self.__MAX_SPEED, relative_x, relative_y)
            if not result:
                return

        # Get Pylance to stop complaining
        assert velocity is not None

        self.__velocity = velocity

    @staticmethod
    def __calculate_global_destination(
        drone_position: location.Location, relative_x: float, relative_y: float
    ) -> location.Location:
        """
        Calculates destination in world.
        """
        destination_x = drone_position.location_x + relative_x
        destination_y = drone_position.location_y + relative_y
        return location.Location(destination_x, destination_y)

    def __set_destination(self, relative_x: float, relative_y: float) -> bool:
        """
        Attempts to set the destination.

        Returns whether successful.
        """
        print("Setting relative destination: " + str(relative_x) + "," + str(relative_y))

        # Drone is halted
        if self.__status != drone_status.DroneStatus.HALTED:
            print("ERROR: Could not set destination, drone is not halted")
            return False

        destination = self.__calculate_global_destination(self.__position, relative_x, relative_y)

        # Destination is within bounds
        is_within_bounds = self.__is_within_boundary(
            destination,
            self.__boundary_top_left,
            self.__boundary_bottom_right,
        )
        if not is_within_bounds:
            print("ERROR: Could not set destination, out of bounds")
            return False

        # Update intent
        self.__update_intent(drone_status.DroneStatus.MOVING, destination)

        return True

    def __halt(self) -> bool:
        """
        Halts the drone.

        Returns whether successful.
        """
        print("Halting")

        # Drone is not landed
        if self.__status == drone_status.DroneStatus.LANDED:
            print("ERROR: Could not halt drone, drone is landed")
            return False

        if self.__status == drone_status.DroneStatus.HALTED:
            print("Warning: Drone is already halted")

        # Update intent
        self.__update_intent(drone_status.DroneStatus.HALTED, self.__position)

        return True

    def __land(self) -> bool:
        """
        Lands the drone.

        Returns whether successful.
        """
        print("Landing")

        # Drone is halted
        if self.__status != drone_status.DroneStatus.HALTED:
            print("ERROR: Could not land, drone is not halted")
            return False

        # Update intent
        self.__update_intent(drone_status.DroneStatus.LANDED, self.__position)

        return True

    def __apply_command(self, command: commands.Command) -> bool:
        """
        Attempts to follow the provided command.

        Returns whether successful.
        """
        command_type = command.get_command_type()
        if command_type == commands.Command.CommandType.SET_RELATIVE_DESTINATION:
            relative_x, relative_y = command.get_relative_destination()
            return self.__set_destination(relative_x, relative_y)

        if command_type == commands.Command.CommandType.HALT:
            return self.__halt()

        if command_type == commands.Command.CommandType.LAND:
            return self.__land()

        print("ERROR: Not a valid command")
        return False

    @staticmethod
    def __is_close(actual: float, expected: float, tolerance: float) -> bool:
        difference = 0
        if actual > expected:
            difference = actual - expected
        else:
            difference = expected - actual

        return difference <= tolerance

    def __is_arrived(self) -> bool:
        """
        Checks whether the drone has arrived at the destination.
        """
        if self.__status != drone_status.DroneStatus.MOVING:
            return False

        position_x = self.__position.location_x
        position_y = self.__position.location_y

        destination_x = self.__destination.location_x
        destination_y = self.__destination.location_y

        velocity_x, velocity_y = self.__velocity.get_xy_velocity()

        # Closeness
        if self.__is_close(position_x, destination_x, self.__acceptance_radius) and self.__is_close(
            position_y, destination_y, self.__acceptance_radius
        ):
            # Required for separation
            return True

        # Overshoot
        # If same sign, drone is still on the way
        if (destination_x - position_x) * velocity_x <= 0.0 and (
            destination_y - position_y
        ) * velocity_y <= 0.0:
            # Required for separation
            return True

        return False

    @staticmethod
    def __set_course(
        speed: float, relative_x: float, relative_y: float
    ) -> "tuple[bool, drone_velocity.DroneVelocity | None]":
        """
        Helm, set course for Earth.
        """
        direction = math.atan2(relative_y, relative_x)

        result, velocity = drone_velocity.DroneVelocity.create(speed, direction)
        if not result:
            message = (
                "ERROR: Could not set course with speed: "
                + str(speed)
                + ", direction: "
                + str(direction)
            )

            print(message)
            return False, None

        return True, velocity

    def run(self, command: commands.Command) -> "tuple[drone_report.DroneReport, int]":
        """
        Advance the simulation by 1 timestep.
        """
        # Commands
        if command.get_command_type() != commands.Command.CommandType.NULL:
            print("Received command")
            self.__commands.append(command)

            result = self.__apply_command(command)
            if not result:
                print("ERROR: Command failed")

        # Sensors
        if self.__is_arrived():
            # Force drone into correct position in case of numerical approximation errors
            self.__position = self.__destination
            self.__update_intent(drone_status.DroneStatus.HALTED, self.__destination)

        # Physical simulation
        # Simple implicit Euler approximation
        velocity_x, velocity_y = self.__velocity.get_xy_velocity()
        self.__position.location_x += velocity_x * self.__time_step_size
        self.__position.location_y += velocity_y * self.__time_step_size

        current_step = self.__current_step
        self.__current_step += 1

        report = drone_report.DroneReport(self.__status, self.__destination, self.__position)
        return report, current_step
