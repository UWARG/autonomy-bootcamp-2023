"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Map go brrr.
"""

import pathlib
import time

import cv2

from modules import location
from modules.private.simulation.mapping import map_render


PIXELS_PER_METRE = 60
IMAGE_RESOLUTION_X = 1200
IMAGE_RESOLUTION_Y = 900
MAP_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/world")
LANDING_PAD_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/assets")
DELAY = 0.01


def display(renderer: map_render.MapRender, position: location.Location) -> bool:
    """
    Helper function.
    """
    result, image = renderer.run(position)
    if not result:
        return False

    # Get Pylance to stop complaining
    assert image is not None

    # Pylint has issues with OpenCV
    # pylint: disable=no-member
    cv2.namedWindow("Map", cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow("Map", image.shape[1] // 2, image.shape[0] // 2)
    cv2.imshow("Map", image)
    cv2.waitKey(1)
    # pylint: enable=no-member

    return True


# Result checking, basic for loops
# pylint: disable-next=too-many-return-statements,too-many-branches
def figure8() -> int:
    """
    main.
    """
    landing_pad_locations = [
        location.Location(0.0, 0.0),
        location.Location(-40.0, 0.5),
    ]

    result, renderer = map_render.MapRender.create(
        PIXELS_PER_METRE,
        IMAGE_RESOLUTION_X,
        IMAGE_RESOLUTION_Y,
        MAP_IMAGES_PATH,
        LANDING_PAD_IMAGES_PATH,
        landing_pad_locations,
    )
    if not result:
        return -1

    # Get Pylance to stop complaining
    assert renderer is not None

    position = location.Location(0.0, 0.0)

    result = display(renderer, position)
    if not result:
        return -1

    # Top right corner
    for _ in range(0, 500):
        position.location_x += 0.1
        position.location_y += 0.075
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    # Bottom right corner
    for _ in range(0, 500):
        position.location_y -= 0.15
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    # Centre
    for _ in range(0, 500):
        position.location_x -= 0.1
        position.location_y += 0.075
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    # Bottom left corner
    for _ in range(0, 500):
        position.location_x -= 0.1
        position.location_y -= 0.075
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    # Top left corner
    for _ in range(0, 500):
        position.location_y += 0.15
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    # Centre
    for _ in range(0, 500):
        position.location_x += 0.1
        position.location_y -= 0.075
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    # Left
    for _ in range(0, 500):
        position.location_x -= 0.1
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    # Centre
    for _ in range(0, 500):
        position.location_x += 0.1
        result = display(renderer, position)
        if not result:
            return -1

        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    status = figure8()
    if status < 0:
        print("ERROR: Status code: " + str(status))

    print("Done!")
