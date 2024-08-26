"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Kinematics calculations.
"""

import math


class DroneVelocity:
    """
    Speed and direction.
    """

    __create_key = object()

    @classmethod
    def create(cls, speed: float, direction: float) -> "tuple[bool, DroneVelocity | None]":
        """
        speed is in m/s .
        direction is in radians between -pi and pi . 0 is in the x direction.
        """
        if not cls.__is_speed_valid(speed):
            return False, None

        if not cls.__is_direction_valid(direction):
            return False, None

        return True, DroneVelocity(cls.__create_key, speed, direction)

    def __init__(self, class_private_create_key, speed: float, direction: float):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DroneVelocity.__create_key, "Use create() method"

        self.__speed = speed
        self.__direction = direction

    @staticmethod
    def __is_speed_valid(speed: float) -> bool:
        """
        Checks if speed is 0.0 or greater.
        """
        return speed >= 0.0

    @staticmethod
    def __is_direction_valid(direction: float) -> bool:
        """
        Checks if direction is between -pi and pi .
        """
        return direction >= -math.pi or direction <= math.pi

    @staticmethod
    def __calculate_xy_velocity(speed: float, direction: float) -> "tuple[float, float]":
        """
        Unit circle.
        """
        velocity_x = speed * math.cos(direction)
        velocity_y = speed * math.sin(direction)
        return velocity_x, velocity_y

    def get_xy_velocity(self) -> "tuple[float, float]":
        """
        Velocity components.
        """
        return self.__calculate_xy_velocity(self.__speed, self.__direction)

    def set_speed(self, speed: float) -> bool:
        """
        speed: New speed in m/s .
        """
        if self.__is_speed_valid(speed):
            return False

        self.__speed = speed

        return True

    def set_direction(self, direction: float) -> bool:
        """
        direction: New direction in radians.
        """
        if self.__is_direction_valid(direction):
            return False

        self.__direction = direction

        return True
