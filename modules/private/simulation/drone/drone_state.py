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

    __TIME_STEP_SIZE = 0.01  # \delta t in seconds
    __MAX_SPEED = 5.0  # m/s
    __ACCEPTANCE_RADIUS = 0.1  # Distance within destination before halting in metres

    @classmethod
    def create(cls,
               initial_x: float,
               initial_y: float,
               boundary1: "tuple[float, float]",
               boundary2: "tuple[float, float]") -> "tuple[bool, DroneState | None]":
        """
        initial is initial position of drone.
        boundary is xyxy corners of map area.
        """
        if len(boundary1) != 2 or len(boundary2) != 2:
            return False, None

        if boundary1[0] >= boundary2[0]:
            return False, None

        if boundary1[1] >= boundary2[0]:
            return False, None

        if initial_x < boundary1[0] or initial_x > boundary2[0]:
            return False, None

        if initial_y < boundary1[1] or initial_y > boundary2[1]:
            return False, None

        return True, DroneState(
            cls.__create_key,
            initial_x,
            initial_y,
            boundary1[0],
            boundary1[1],
            boundary2[0],
            boundary2[1])

    # Better to be explicit with parameters
    # pylint: disable-next=too-many-arguments
    def __init__(self,
                 class_private_create_key,
                 initial_x: float,
                 initial_y: float,
                 boundary_x1: float,
                 boundary_y1: float,
                 boundary_x2: float,
                 boundary_y2: float):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneState.__create_key, "Use create() method"

        # Map area boundary
        self.__boundary_x1 = boundary_x1
        self.__boundary_y1 = boundary_y1
        self.__boundary_x2 = boundary_x2
        self.__boundary_y2 = boundary_y2

        # Simulation state
        self.__current_step: int = 0

        # Intent state
        self.__status = drone_status.DroneStatus.HALTED
        self.__destination = location.Location(initial_x, initial_y)  # In world space
        self.__commands = []  # List of all commands received by the drone

        # Physical state
        _, velocity = drone_velocity.DroneVelocity.create(0.0, 0.0)
        assert velocity is not None
        self.__velocity: drone_velocity.DroneVelocity = velocity
        self.__position = location.Location(initial_x, initial_y)

    def __update_intent(self,
                        status: drone_status.DroneStatus,
                        destination: location.Location):
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
    def __calculate_global_destination(drone_position: location.Location,
                                       relative_x: float,
                                       relative_y: float) -> location.Location:
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
        print("Setting relative destination: " + str(relative_x) + ", " + str(relative_y))

        # Drone is halted
        if self.__status != drone_status.DroneStatus.HALTED:
            print("ERROR: Could not set destination, drone is not halted")
            return False

        destination = self.__calculate_global_destination(
            self.__position,
            relative_x,
            relative_y
        )

        destination_x = destination.location_x
        destination_y = destination.location_y

        # Destination is within bounds
        if destination_x < self.__boundary_x1 or destination_x > self.__boundary_x2:
            print("ERROR: Could not set destination, out of bounds")
            return False

        if destination_y < self.__boundary_y1 or destination_y > self.__boundary_y2:
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

        if not self.__is_close(position_x, destination_x, self.__ACCEPTANCE_RADIUS):
            return False

        if not self.__is_close(position_y, destination_y, self.__ACCEPTANCE_RADIUS):
            return False

        return True

    @staticmethod
    def __set_course(speed: float,
                     relative_x: float,
                     relative_y: float) -> "tuple[bool, drone_velocity.DroneVelocity | None]":
        """
        Helm, set course for Earth.
        """
        direction = math.atan2(relative_y, relative_x)

        result, velocity = drone_velocity.DroneVelocity.create(speed, direction)
        if not result:
            message = "ERROR: Could not set course with speed: " \
                           + str(speed) \
                           + ", direction: " \
                           + str(direction)

            print(message)
            return False, None

        return True, velocity

    def run(self, command: "commands.Command | None") -> "tuple[drone_report.DroneReport, int]":
        """
        Advance the simulation by 1 timestep.
        """
        # Commands
        if command is not None:
            print("Received command")
            self.__commands.append(command)

            result = self.__apply_command(command)
            if not result:
                print("ERROR: Command failed")

        # Sensors
        if self.__is_arrived():
            self.__update_intent(drone_status.DroneStatus.HALTED, self.__destination)

        # Physical simulation
        # Simple implicit Euler approximation
        velocity_x, velocity_y = self.__velocity.get_xy_velocity()
        self.__position.location_x += velocity_x * self.__TIME_STEP_SIZE
        self.__position.location_y += velocity_y * self.__TIME_STEP_SIZE

        current_step = self.__current_step
        self.__current_step += 1

        report = drone_report.DroneReport(self.__status, self.__destination, self.__position)
        return report, current_step
