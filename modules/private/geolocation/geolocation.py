"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Very simplified localization.
"""

from ... import bounding_box
from ... import drone_report
from ... import location


class Geolocation:
    """
    Simple class to convert pixel coordinates to world coordinates.
    Basically does the reverse of the simulator.
    Camera is straight down without rotation.
    """

    __create_key = object()

    @classmethod
    def create(
        cls, pixels_per_metre: int, resolution_x: int, resolution_y: int
    ) -> "tuple[bool, Geolocation | None]":
        """
        pixels_per_metre: Assumes square pixels.
        """
        if resolution_x < 1:
            return False, None

        if resolution_y < 1:
            return False, None

        if pixels_per_metre < 1:
            return False, None

        return True, Geolocation(cls.__create_key, pixels_per_metre, resolution_x, resolution_y)

    def __init__(
        self, class_private_create_key, pixels_per_metre: int, resolution_x: int, resolution_y: int
    ):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Geolocation.__create_key, "Use create() method"

        self.__pixels_per_metre = pixels_per_metre

        self.__resolution_x = resolution_x
        self.__resolution_y = resolution_y

    @staticmethod
    # Better to be explicit with parameters
    # pylint: disable-next=too-many-arguments
    def __position_from_pixel_coordinates(
        pixels_per_metre: int,
        resolution_x: int,
        resolution_y: int,
        pixel_x: float,
        pixel_y: float,
        camera_position: location.Location,
    ) -> location.Location:
        """
        Gets the relative position.
        """
        position_x = (pixel_x - resolution_x / 2) / pixels_per_metre + camera_position.location_x
        # Positive y is up
        position_y = -(pixel_y - resolution_y / 2) / pixels_per_metre + camera_position.location_y

        return location.Location(position_x, position_y)

    def run(
        self, report: drone_report.DroneReport, bounding_boxes: "list[bounding_box.BoundingBox]"
    ) -> "list[location.Location]":
        """
        Converts the centre of bounding boxes into locations on the map.
        """
        camera_position = report.position

        landing_pad_positions = []
        for box in bounding_boxes:
            centre_pixel_x, centre_pixel_y = box.get_centre()
            position = self.__position_from_pixel_coordinates(
                self.__pixels_per_metre,
                self.__resolution_x,
                self.__resolution_y,
                centre_pixel_x,
                centre_pixel_y,
                camera_position,
            )
            landing_pad_positions.append(position)

        return landing_pad_positions
