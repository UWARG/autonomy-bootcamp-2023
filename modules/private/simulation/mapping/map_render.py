"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Renders the image seen by the camera.
"""
import pathlib

import cv2
import numpy as np

from .... import location


# Basically a struct
# pylint: disable-next=too-few-public-methods
class LandingPadOnMap:
    """
    Information required to draw the landing pad on the combined image.
    """
    __create_key = object()

    @classmethod
    # Better to be explicit with parameters, required by checks
    # pylint: disable-next=too-many-arguments,too-many-return-statements
    def create(cls,
               pixels_per_metre: int,
               pad_image: np.ndarray,
               pad_position: location.Location,
               resolution_x: int,
               resolution_y: int) -> "tuple[bool, LandingPadOnMap | None]":
        """
        Data to draw the landing pad on the combined local map.
        """
        if pixels_per_metre < 1:
            return False, None

        if resolution_x < 1:
            return False, None

        if resolution_y < 1:
            return False, None

        if len(pad_image.shape) < 3:
            return False, None

        # Alpha channel
        if pad_image.shape[2] != 4:
            return False, None

        result, pixel_location = MapRender.world_pixel_from_position_coordinates(
            pad_position,
            pixels_per_metre,
        )
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert pixel_location is not None

        pixel_x, pixel_y = pixel_location

        result, image_location = MapRender.image_from_pixel_coordinates(
            pixel_x,
            pixel_y,
            resolution_x,
            resolution_y,
        )
        if not result:
            return False, None

        # Get Pylance to stop complaining
        assert image_location is not None

        image_x, image_y = image_location

        return True, LandingPadOnMap(
            cls.__create_key,
            pad_image,
            image_x,
            image_y,
            pixel_x % resolution_x,
            pixel_y % resolution_y,
        )

    # Better to be explicit with parameters
    # pylint: disable-next=too-many-arguments
    def __init__(self,
                 class_private_create_key,
                 pad_image: np.ndarray,
                 image_x: int,
                 image_y: int,
                 centre_pixel_x: int,
                 centre_pixel_y: int):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is LandingPadOnMap.__create_key, "Use create() method"

        self.pad_image = pad_image
        self.image_x = image_x
        self.image_y = image_y
        self.centre_pixel_x = centre_pixel_x
        self.centre_pixel_y = centre_pixel_y


class CombinedLocalMap:
    """
    9 map images combined together.
    """
    __create_key = object()

    @classmethod
    def create(cls,
               centre_image_x: int,
               centre_image_y: int,
               named_images: "dict[tuple[int, int], np.ndarray]",
               landing_pads: "list[LandingPadOnMap]") \
        -> "tuple[bool, CombinedLocalMap | None]":
        """
        Combines the centre image and the images around it, and draws the landing pads.
        """
        # Combine images
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

        # Draw landing pads
        for landing_pad in landing_pads:
            # Pixel offset = Image corner in pixels + offset inside image
            offset_x = (landing_pad.image_x - centre_image_x + 1) * combined_image.shape[1] // 3 \
                + landing_pad.centre_pixel_x - landing_pad.pad_image.shape[1] // 2
            offset_y = (landing_pad.image_y - centre_image_y + 1) * combined_image.shape[0] // 3 \
                + landing_pad.centre_pixel_y - landing_pad.pad_image.shape[0] // 2

            result, _ = cls.__add_transparent_image(
                combined_image,
                landing_pad.pad_image,
                offset_x,
                offset_y,
            )
            if not result:
                return False, None

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
    # Original code
    # pylint: disable-next=too-many-locals
    def __add_transparent_image(background: np.ndarray,
                                foreground: np.ndarray,
                                x_offset: int,
                                y_offset: int) -> "tuple[bool, bool | None]":
        """
        Correctly overlays the possibly transparent foreground image onto the background image.
        From: https://stackoverflow.com/a/71701023
        Modified for WARG use.

        background: Image to be mutated.

        Return: Status, whether it was drawn.
        """
        bg_h, bg_w, bg_channels = background.shape
        fg_h, fg_w, fg_channels = foreground.shape

        # Original code
        # pylint: disable=line-too-long
        # assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
        # assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'
        # pylint: enable=line-too-long
        if bg_channels != 3:
            print("ERROR: Background does not have 3 colour channels")
            return False, None

        if fg_channels != 4:
            print("ERROR: Foreground does not have 4 colour channels")
            return False, None

        # center by default
        # if x_offset is None: x_offset = (bg_w - fg_w) // 2
        # if y_offset is None: y_offset = (bg_h - fg_h) // 2

        # Original code
        # pylint: disable=invalid-name
        w: int = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
        h: int = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)
        # pylint: enable=invalid-name

        if w < 1 or h < 1:
            return True, False

        # clip foreground and background images to the overlapping regions
        bg_x = max(0, x_offset)
        bg_y = max(0, y_offset)
        fg_x = max(0, x_offset * -1)
        fg_y = max(0, y_offset * -1)
        foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
        background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

        # separate alpha and color channels from the foreground image
        foreground_colors = foreground[:, :, :3]
        alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

        # construct an alpha_mask that matches the image shape
        # alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
        # Optimization from comment
        alpha_mask = alpha_channel[:,:,np.newaxis]

        # combine the background with the overlay image weighted by alpha
        composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

        # overwrite the section of the background image that has been updated
        background[bg_y:bg_y + h, bg_x:bg_x + w] = composite

        return True, True

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
        top = centre_pixel_y - resolution_y // 2 + resolution_y
        bottom = centre_pixel_y + (resolution_y + 1) // 2 + resolution_y
        left = centre_pixel_x - resolution_x // 2 + resolution_x
        right = centre_pixel_x + (resolution_x + 1) // 2 + resolution_x

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


# Better to be explicit with members
# pylint: disable-next=too-many-instance-attributes
class MapRender:
    """
    Loads, concatenats, crops, and displays map images.
    Uses caching to reduce memory usage.
    """
    __create_key = object()

    __DEFAULT_MAP_IMAGE_NAME = "default.png"
    __LANDING_PAD_IMAGE_NAME = "landing_pad.png"

    @classmethod
    # Better to be explicit with parameters, required by checks, required by checks
    # pylint: disable-next=too-many-arguments,too-many-return-statements,too-many-branches
    def create(cls,
               pixels_per_metre: int,
               resolution_x: int,
               resolution_y: int,
               map_image_directory: pathlib.Path,
               landing_pad_image_directory: pathlib.Path,
               landing_pad_locations: "list[location.Location]") -> "tuple[bool, MapRender | None]":
        """
        pixels_per_metre: Number of pixels for each metre of distance.
        resolution is resolution of images in pixels.
        map_image_directory: Directory containing the map images.
        """
        if pixels_per_metre < 1:
            return False, None

        if resolution_x < 1:
            return False, None

        if resolution_y < 1:
            return False, None

        if not map_image_directory.is_dir():
            return False, None

        if not landing_pad_image_directory.is_dir():
            return False, None

        default_map_image_path = pathlib.Path(
            map_image_directory,
            cls.__DEFAULT_MAP_IMAGE_NAME,
        )
        if not default_map_image_path.exists():
            return False, None

        # Pylint has issues with OpenCV
        # pylint: disable-next=no-member
        default_map_image = cv2.imread(str(default_map_image_path))
        if default_map_image is None:
            return False, None

        # Get Pylance to stop complaining
        assert default_map_image is not None

        if not cls.__is_image_valid_shape(default_map_image, (resolution_y, resolution_x, 3)):
            return False, None

        landing_pad_image_path = pathlib.Path(
            landing_pad_image_directory,
            cls.__LANDING_PAD_IMAGE_NAME,
        )
        if not landing_pad_image_path.exists():
            return False, None

        # Pylint has issues with OpenCV
        # pylint: disable-next=no-member
        landing_pad_image = cv2.imread(str(landing_pad_image_path), cv2.IMREAD_UNCHANGED)
        if landing_pad_image is None:
            return False, None

        # Get Pylance to stop complaining
        assert landing_pad_image is not None

        if len(landing_pad_image.shape) != 3:
            return False, None

        if landing_pad_image.shape[1] > resolution_x // 2:
            return False, None

        if landing_pad_image.shape[0] > resolution_y // 2:
            return False, None

        if landing_pad_image.shape[2] != 4:
            return False, None

        landing_pads = []
        for landing_pad_location in landing_pad_locations:
            result, landing_pad_on_map = LandingPadOnMap.create(
                pixels_per_metre,
                landing_pad_image,
                landing_pad_location,
                resolution_x,
                resolution_y
            )
            if not result:
                return False, None

            # Get Pylance to stop complaining
            assert landing_pad_on_map is not None

            landing_pads.append(landing_pad_on_map)

        return True, MapRender(
            cls.__create_key,
            pixels_per_metre,
            resolution_x,
            resolution_y,
            map_image_directory,
            default_map_image,
            landing_pads,
        )

    # Better to be explicit with parameters
    # pylint: disable-next=too-many-arguments
    def __init__(self,
                 class_private_create_key,
                 pixels_per_metre: int,
                 resolution_x: int,
                 resolution_y: int,
                 map_image_directory: pathlib.Path,
                 default_map_image: np.ndarray,
                 landing_pads: "list[LandingPadOnMap]"):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is MapRender.__create_key, "Use create() method"

        self.__pixels_per_metre = pixels_per_metre
        self.__resolution_x = resolution_x
        self.__resolution_y = resolution_y

        self.__map_image_directory = map_image_directory
        self.__default_map_image = default_map_image

        self.__cached_images: "dict[tuple[int, int], np.ndarray]" = {}
        self.__current_render: "CombinedLocalMap | None" = None
        self.__landing_pads = landing_pads

    @staticmethod
    def __is_image_valid_shape(image: np.ndarray, shape: "tuple[int, int, int]"):
        """
        Check to ensure loaded image is correct shape.
        """
        return image.shape == shape

    @staticmethod
    def image_from_pixel_coordinates(pixel_x: int,
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
    def world_pixel_from_position_coordinates(position: location.Location,
                                              pixels_per_metre: int) \
        -> "tuple[bool, tuple[int, int] | None]":
        """
        Camera space to pixel space.
        Truncates rather than rounds.
        """
        if pixels_per_metre < 1:
            return False, None

        # In image space, positive y is down
        pixel_x = int(position.location_x * pixels_per_metre)
        pixel_y = int(position.location_y * pixels_per_metre * -1)

        return True, (pixel_x, pixel_y)

    @staticmethod
    def __generate_default_map_image_with_coordinates(image: np.ndarray,
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
            (image.shape[1] // 8, image.shape[0] // 2),
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
        image_path = pathlib.Path(self.__map_image_directory, image_name)
        if image_path.exists():
            # Pylint has issues with OpenCV
            # pylint: disable-next=no-member
            image = cv2.imread(str(image_path))
        else:
            print("Warning: Could not read image file: " + image_path.name)
            print("Warning: Loading default")
            self.__cached_images[(image_x, image_y)] = \
                self.__generate_default_map_image_with_coordinates(
                    self.__default_map_image,
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
                self.__generate_default_map_image_with_coordinates(
                    self.__default_map_image,
                    image_x,
                    image_y,
                )
            return

        self.__cached_images[(image_x, image_y)] = image

    def run(self, camera_position: location.Location) -> "tuple[bool, np.ndarray | None]":
        """
        Returns the map image seen by the camera.
        """
        result, pixel_location = self.world_pixel_from_position_coordinates(
            camera_position,
            self.__pixels_per_metre,
        )
        if not result:
            print("ERROR: Could not get pixel coordinates")
            return False, None

        # Get Pylance to stop complaining
        assert pixel_location is not None

        pixel_x, pixel_y = pixel_location

        result, image_to_load = self.image_from_pixel_coordinates(
            pixel_x,
            pixel_y,
            self.__resolution_x,
            self.__resolution_y,
        )
        if not result:
            print("ERROR: Could not determine image to load")
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
                self.__landing_pads,
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
                self.__landing_pads,
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
