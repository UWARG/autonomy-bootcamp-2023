"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test generate destination.
"""

import random

from modules import location
from modules.private import generate_destination


PIXELS_PER_METRE = 60
IMAGE_RESOLUTION_X = 1200
IMAGE_RESOLUTION_Y = 900

DISTANCE_IMAGE_X = IMAGE_RESOLUTION_X / PIXELS_PER_METRE
DISTANCE_IMAGE_Y = IMAGE_RESOLUTION_Y / PIXELS_PER_METRE

TEST_COUNT = 1000


if __name__ == "__main__":
    random.seed()

    drone_initial_position = location.Location(0.0, 0.0)

    boundary_bottom_left = location.Location(
        -1.5 * DISTANCE_IMAGE_X - 0.1,
        -1.5 * DISTANCE_IMAGE_Y - 0.1,
    )
    boundary_top_right = location.Location(
        1.5 * DISTANCE_IMAGE_X + 0.1,
        1.5 * DISTANCE_IMAGE_Y + 0.1,
    )

    for i in range(0, TEST_COUNT):
        # Access required for test
        # pylint: disable=protected-access
        result, waypoint = generate_destination.__generate_waypoint(  # type: ignore
            drone_initial_position,
            boundary_bottom_left,
            boundary_top_right,
            PIXELS_PER_METRE,
            IMAGE_RESOLUTION_X,
            IMAGE_RESOLUTION_Y,
        )
        assert result
        assert waypoint is not None

        assert waypoint.location_x >= boundary_bottom_left.location_x
        assert waypoint.location_x <= boundary_top_right.location_x
        assert waypoint.location_y >= boundary_bottom_left.location_y
        assert waypoint.location_y <= boundary_top_right.location_y

        if -DISTANCE_IMAGE_X < waypoint.location_x < DISTANCE_IMAGE_X:
            assert abs(waypoint.location_y) >= DISTANCE_IMAGE_Y

        elif -DISTANCE_IMAGE_Y < waypoint.location_y < DISTANCE_IMAGE_Y:
            assert abs(waypoint.location_x) >= DISTANCE_IMAGE_X

    waypoint_position = location.Location(10.0, -7.5)
    for i in range(0, TEST_COUNT):
        # Access required for test
        # pylint: disable=protected-access
        result, landing_pad = generate_destination.__generate_landing_pad(  # type: ignore
            waypoint_position,
            PIXELS_PER_METRE,
            IMAGE_RESOLUTION_X,
            IMAGE_RESOLUTION_Y,
        )
        assert result
        assert landing_pad is not None
        assert landing_pad.location_x >= 0.0
        assert landing_pad.location_x <= 20.0
        assert landing_pad.location_y >= -15.0
        assert landing_pad.location_y <= 0.0

    print("Done!")
