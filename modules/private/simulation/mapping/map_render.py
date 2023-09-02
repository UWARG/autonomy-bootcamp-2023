"""
DO NOT MODIFY THIS FILE.

Renders the image seen by the camera.
"""
import pathlib

import cv2
import numpy as np


class CombinedLocalMap:
    """
    9 map images combined together.
    """
    __create_key = object()

    @classmethod
    def create(cls,
               centre_image_x: int,
               centre_image_y: int,
               named_images: "dict[tuple[int, int], np.ndarray]") \
        -> "tuple[bool, CombinedLocalMap | None]":
        """
        Combines the centre image and the images to the top left.
        """
        columns = []
        for i in range(centre_image_x - 1, centre_image_x + 1 + 1):
            row = []
            for j in range(centre_image_y - 1, centre_image_y + 1 + 1):
                image = named_images.get((i, j))
                if image is None:
                    return False, None

                row.append(image)

            column = np.concatenate(tuple(row), axis=0)
            columns.append(column)

        combined_image = np.concatenate(tuple(columns), axis=1)

        return True, CombinedLocalMap(
            cls.__create_key,
            centre_image_x,
            centre_image_y,
            combined_image,
        )

    def __init__(self,
                 class_private_create_key,
                 centre_image_x: int,
                 centre_image_y: int,
                 combined_image: np.ndarray):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is CombinedLocalMap.__create_key, "Use create() method"

        self.centre_image_x = centre_image_x
        self.centre_image_y = centre_image_y
        self.__combined_image = combined_image

    @staticmethod
    def __is_within_bounds(to_check: int, lower: int, upper: int) -> bool:
        """
        Inclusive.
        """
        if to_check < lower:
            return False

        if to_check > upper:
            return False

        return True

    # Required by checks
    # pylint: disable-next=too-many-return-statements
    def get_view(self,
                 centre_pixel_x: int,
                 centre_pixel_y: int,
                 resolution_x: int,
                 resolution_y: int) -> "tuple[bool, np.ndarray | None]":
        """
        Window into larger image.
        """
        # Offset from centre
        top = centre_pixel_y - int(resolution_y / 2) + resolution_y
        bottom = centre_pixel_y + int((resolution_y + 1) / 2) + resolution_y
        left = centre_pixel_x - int(resolution_x / 2) + resolution_x
        right = centre_pixel_x + int((resolution_x + 1) / 2) + resolution_x

        # Positive y is down
        if top >= bottom:
            return False, None

        if left >= right:
            return False, None

        if not self.__is_within_bounds(top, 0, self.__combined_image.shape[0]):
            return False, None

        if not self.__is_within_bounds(bottom, 0, self.__combined_image.shape[0]):
            return False, None

        if not self.__is_within_bounds(left, 0, self.__combined_image.shape[1]):
            return False, None

        if not self.__is_within_bounds(right, 0, self.__combined_image.shape[1]):
            return False, None

        return True, np.array(self.__combined_image[top:bottom,left:right])


class MapRender:
    """
    Loads, concatenats, crops, and displays map images.
    Uses caching to reduce memory usage.
    """
    __create_key = object()

    __DEFAULT_IMAGE_NAME = "default.png"

    @classmethod
    # Required by checks
    # pylint: disable-next=too-many-return-statements
    def create(cls,
               pixels_per_metre: int,
               resolution_x: int,
               resolution_y: int,
               image_directory: pathlib.Path) -> "tuple[bool, MapRender | None]":
        """
        pixels_per_metre: Number of pixels for each metre of distance.
        resolution is resolution of images in pixels.
        image_directory: Directory containing the map images.
        """
        if pixels_per_metre < 1:
            return False, None

        if resolution_x < 1:
            return False, None

        if resolution_y < 1:
            return False, None

        if not image_directory.is_dir():
            return False, None

        default_image_path = pathlib.PurePosixPath(image_directory, cls.__DEFAULT_IMAGE_NAME)
        # Pylint has issues with OpenCV
        # pylint: disable-next=no-member
        default_image = cv2.imread(str(default_image_path))
        if default_image is None:
            return False, None

        # Get Pylance to stop complaining
        assert default_image is not None

        if not cls.__is_image_valid_shape(default_image, (resolution_y, resolution_x, 3)):
            return False, None

        return True, MapRender(
            cls.__create_key,
            pixels_per_metre,
            resolution_x,
            resolution_y,
            image_directory,
            default_image,
        )

    # Better to be explicit with parameters
    # pylint: disable-next=too-many-arguments
    def __init__(self,
                 class_private_create_key,
                 pixels_per_metre: int,
                 resolution_x: int,
                 resolution_y: int,
                 image_directory: pathlib.Path,
                 default_image: np.ndarray):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is MapRender.__create_key, "Use create() method"

        self.__pixels_per_metre = pixels_per_metre
        self.__resolution_x = resolution_x
        self.__resolution_y = resolution_y

        self.__image_directory = image_directory
        self.__default_image = default_image

        self.__cached_images: "dict[tuple[int, int], np.ndarray]" = {}
        self.__current_render: "CombinedLocalMap | None" = None

    @staticmethod
    def __is_image_valid_shape(image: np.ndarray, shape: "tuple[int, int, int]"):
        """
        Check to ensure loaded image is correct shape.
        """
        return image.shape == shape

    @staticmethod
    def __image_from_pixel_coordinates(pixel_x: int,
                                       pixel_y: int,
                                       resolution_x: int,
                                       resolution_y: int) -> "tuple[bool, tuple[int, int] | None]":
        """
        Calculates the appropriate image to load.
        """
        if resolution_x < 1:
            return False, None

        if resolution_y < 1:
            return False, None

        # Integer division always rounds to the lesser number (floor division)
        image_x = pixel_x // resolution_x
        image_y = pixel_y // resolution_y

        return True, (image_x, image_y)

    @staticmethod
    def __pixel_from_position_coordinates(position_x: float,
                                          position_y: float,
                                          pixels_per_metre: int) \
        -> "tuple[bool, tuple[int, int] | None]":
        """
        Camera space to pixel space.
        Truncates rather than rounds.
        """
        if pixels_per_metre < 1:
            return False, None

        # In image space, positive y is down
        pixel_x = int(position_x * pixels_per_metre)
        pixel_y = int(position_y * pixels_per_metre * -1)

        return True, (pixel_x, pixel_y)

    @staticmethod
    def __generate_default_image_with_coordinates(image: np.ndarray,
                                                  image_x: int,
                                                  image_y: int) -> np.ndarray:
        """
        Writes the coordinates on the image.
        """
        text = str(image_x) + "," + str(image_y)
        # Pylint has issues with OpenCV
        # pylint: disable-next=no-member
        image = cv2.putText(
            np.array(image, dtype=np.uint8),
            text,
            (int(image.shape[1] / 8), int(image.shape[0] / 2)),
            # Pylint has issues with OpenCV
            # pylint: disable-next=no-member
            cv2.FONT_HERSHEY_SIMPLEX,
            9.0,
            (0, 0, 0),
            9,
        )

        return image

    def __evict_image_from_cache(self, image_x: int, image_y: int):
        image = self.__cached_images.get((image_x, image_y))
        if image is None:
            return

        del self.__cached_images[(image_x, image_y)]

    def __load_image_into_cache(self, image_x: int, image_y: int):
        """
        Loads the appropriate image.
        Looks in cache and on failure then reads file.
        """
        image = self.__cached_images.get((image_x, image_y))
        # Cache hit, nothing to do
        if image is not None:
            return

        # Cache miss, load from file
        image_name = str(image_x) + "," + str(image_y) + ".png"
        image_path = pathlib.PurePosixPath(self.__image_directory, image_name)
        # Pylint has issues with OpenCV
        # pylint: disable-next=no-member
        image = cv2.imread(str(image_path))
        if image is None:
            print("Warning: Could not read image file: " + image_path.name)
            print("Warning: Loading default")
            self.__cached_images[(image_x, image_y)] = \
                self.__generate_default_image_with_coordinates(
                    self.__default_image,
                    image_x,
                    image_y,
                )
            return

        # Get Pylance to stop complaining
        assert image is not None

        if image.shape != (self.__resolution_y, self.__resolution_x, 3):
            print("Warning: Image has incorrect shape: " + str(image.shape))
            print("Warning: Loading default")
            self.__cached_images[(image_x, image_y)] = \
                self.__generate_default_image_with_coordinates(
                    self.__default_image,
                    image_x,
                    image_y,
                )
            return

        self.__cached_images[(image_x, image_y)] = image

    def run(self, camera_x: float, camera_y: float) -> "tuple[bool, np.ndarray | None]":
        """
        Returns the image to be rendered.
        """
        result, pixel_location = self.__pixel_from_position_coordinates(
            camera_x,
            camera_y,
            self.__pixels_per_metre,
        )
        if not result:
            print("ERROR: Could not get pixel coordinates")
            return False, None

        # Get Pylance to stop complaining
        assert pixel_location is not None

        pixel_x, pixel_y = pixel_location

        result, image_to_load = self.__image_from_pixel_coordinates(
            pixel_x,
            pixel_y,
            self.__resolution_x,
            self.__resolution_y,
        )
        if not result:
            print("ERROR: Could determine image")
            return False, None

        # Get Pylance to stop complaining
        assert image_to_load is not None

        centre_image_x, centre_image_y = image_to_load

        # Start at centre-right, anticlockwise
        images_to_load = [
            (centre_image_x + 1, centre_image_y),
            (centre_image_x + 1, centre_image_y + 1),
            (centre_image_x, centre_image_y + 1),
            (centre_image_x - 1, centre_image_y + 1),
            (centre_image_x - 1, centre_image_y),
            (centre_image_x - 1, centre_image_y - 1),
            (centre_image_x, centre_image_y - 1),
            (centre_image_x + 1, centre_image_y - 1),
            (centre_image_x, centre_image_y),  # Centre
        ]

        # L-infinity norm of 3 (satisfies (max(x, y) == 3))
        # Start at centre-right, anticlockwise
        images_to_unload = [
            (centre_image_x + 3, centre_image_y),
            (centre_image_x + 3, centre_image_y + 1),
            (centre_image_x + 3, centre_image_y + 2),
            (centre_image_x + 3, centre_image_y + 3),
            (centre_image_x + 2, centre_image_y + 3),
            (centre_image_x + 1, centre_image_y + 3),
            (centre_image_x, centre_image_y + 3),
            (centre_image_x - 1, centre_image_y + 3),
            (centre_image_x - 2, centre_image_y + 3),
            (centre_image_x - 3, centre_image_y + 3),
            (centre_image_x - 3, centre_image_y + 2),
            (centre_image_x - 3, centre_image_y + 1),
            (centre_image_x - 3, centre_image_y),
            (centre_image_x - 3, centre_image_y - 1),
            (centre_image_x - 3, centre_image_y - 2),
            (centre_image_x - 3, centre_image_y - 3),
            (centre_image_x - 2, centre_image_y - 3),
            (centre_image_x - 1, centre_image_y - 3),
            (centre_image_x, centre_image_y - 3),
            (centre_image_x + 1, centre_image_y - 3),
            (centre_image_x + 2, centre_image_y - 3),
            (centre_image_x + 3, centre_image_y - 3),
            (centre_image_x + 3, centre_image_y - 2),
            (centre_image_x + 3, centre_image_y - 1),
        ]

        # Unload before load
        for image_x, image_y in images_to_unload:
            self.__evict_image_from_cache(image_x, image_y)

        for image_x, image_y in images_to_load:
            self.__load_image_into_cache(image_x, image_y)

        if self.__current_render is None:
            result, self.__current_render = CombinedLocalMap.create(
                centre_image_x,
                centre_image_y,
                self.__cached_images,
            )
            if not result:
                print("ERROR: Could not render map")
                return False, None

        # Get Pylance to stop complaining
        assert self.__current_render is not None

        if centre_image_x != self.__current_render.centre_image_x \
            or centre_image_y != self.__current_render.centre_image_y:
            # Required for separation
            result, self.__current_render = CombinedLocalMap.create(
                centre_image_x,
                centre_image_y,
                self.__cached_images,
            )
            if not result:
                print("ERROR: Could not render map")
                return False, None

        # Get Pylance to stop complaining
        assert self.__current_render is not None

        result, display_image = self.__current_render.get_view(
            pixel_x % self.__resolution_x,
            pixel_y % self.__resolution_y,
            self.__resolution_x,
            self.__resolution_y,
        )
        if not result:
            print("ERROR: Could not render view of map")
            return False, None

        return True, display_image
