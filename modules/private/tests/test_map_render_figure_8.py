"""
DO NOT MODIFY THIS FILE.

Map go brrr.
"""
import pathlib
import time

import cv2

from modules.private.simulation.mapping import map_render


MAP_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/world")


def display(renderer: map_render.MapRender, position_x: float, position_y: float) -> bool:
    """
    Helper function.
    """
    result, image = renderer.run(position_x, position_y)
    if not result:
        return False

    # Get Pylance to stop complaining
    assert image is not None

    # Pylint has issues with OpenCV
    # pylint: disable=no-member
    cv2.namedWindow("Map", cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('Map', 600, 450)
    cv2.imshow("Map", image)
    cv2.waitKey(1)
    # pylint: enable=no-member

    return True


def figure8() -> int:
    """
    main.
    """
    result, renderer = map_render.MapRender.create(
        60,
        1200,
        900,
        MAP_IMAGES_PATH,
    )
    if not result:
        print("Attempt")
        return -1

    # Get Pylance to stop complaining
    assert renderer is not None

    position_x = 0.0
    position_y = 0.0

    result = display(renderer, position_x, position_y)
    if not result:
        return -1

    # Top right corner
    for _ in range(0, 500):
        position_x += 0.1
        position_y += 0.075
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    # Bottom right corner
    for _ in range(0, 500):
        position_y -= 0.15
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    # Centre
    for _ in range(0, 500):
        position_x -= 0.1
        position_y += 0.075
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    # Bottom left corner
    for _ in range(0, 500):
        position_x -= 0.1
        position_y -= 0.075
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    # Top left corner
    for _ in range(0, 500):
        position_y += 0.15
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    # Centre
    for _ in range(0, 500):
        position_x += 0.1
        position_y -= 0.075
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    # Left
    for _ in range(0, 500):
        position_x -= 0.1
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    # Centre
    for _ in range(0, 500):
        position_x += 0.1
        result = display(renderer, position_x, position_y)
        if not result:
            return -1

        time.sleep(0.01)

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    status = figure8()
    if status < 0:
        print("ERROR: Status code: " + str(status))

    print("Done!")
