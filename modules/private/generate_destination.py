"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Randomly generates destination waypoint and landing pad(s).
"""
import pathlib
import random
import time

from .. import location


LOG_FILE_DIRECTORY = pathlib.Path("log")


def __log_seed(seed: "int | None"):
    """
    Logs the seed at the beginning of the program for future reproducibility.
    """
    seed_text = str(seed)
    print("Log seed: " + seed_text)

    LOG_FILE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    file_name = str(int(time.time())) + "_seed.txt"
    file_path = pathlib.Path(LOG_FILE_DIRECTORY, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(seed_text)


def __random_between_with_exclusion(lower_bound: float,
                                    upper_bound: float,
                                    exclusion_lower: float,
                                    exclusion_upper: float) -> "tuple[bool, float | None]":
    """
    Generates a random number between the bounds (inclusive) with exclusion zone (inclusive).
    """
    if lower_bound >= upper_bound:
        return False, None

    if exclusion_lower >= exclusion_upper:
        return False, None

    if exclusion_lower <= lower_bound:
        return False, None

    if exclusion_upper >= upper_bound:
        return False, None

    value = random.uniform(lower_bound, upper_bound)
    while exclusion_lower < value < exclusion_upper:
        value = random.uniform(lower_bound, upper_bound)

    return True, value


# Better to be explicit with parameters
# pylint: disable-next=too-many-arguments
def __generate_waypoint(drone_initial_position: location.Location,
                        boundary_bottom_left: location.Location,
                        boundary_top_right: location.Location,
                        pixels_per_metre: int,
                        resolution_x: int,
                        resolution_y: int) -> "tuple[bool, location.Location | None]":
    """
    Generate a waypoint within the boundary and away from the initial position.
    """
    distance_image_x = resolution_x / pixels_per_metre
    distance_image_y = resolution_y / pixels_per_metre

    result, waypoint_x = __random_between_with_exclusion(
        boundary_bottom_left.location_x + distance_image_x / 2,
        boundary_top_right.location_x - distance_image_x / 2,
        drone_initial_position.location_x - distance_image_x,
        drone_initial_position.location_x + distance_image_x,
    )
    if not result:
        return False, None

    # Get Pylance to stop complaining
    assert waypoint_x is not None

    result, waypoint_y = __random_between_with_exclusion(
        boundary_bottom_left.location_y + distance_image_y / 2,
        boundary_top_right.location_y - distance_image_y / 2,
        drone_initial_position.location_y - distance_image_y,
        drone_initial_position.location_y + distance_image_y,
    )
    if not result:
        return False, None

    # Get Pylance to stop complaining
    assert waypoint_y is not None

    return True, location.Location(waypoint_x, waypoint_y)


def __generate_landing_pad(waypoint_position: location.Location,
                           pixels_per_metre: int,
                           resolution_x: int,
                           resolution_y: int) -> "tuple[bool, location.Location | None]":
    """
    Generate landing pad location around the waypoint position.
    """
    if pixels_per_metre < 1:
        return False, None

    if resolution_x < 1:
        return False, None

    if resolution_y < 1:
        return False, None

    distance_image_x = resolution_x / pixels_per_metre
    distance_image_y = resolution_y / pixels_per_metre

    local_x = random.uniform(
        -distance_image_x / 2 + 1.0,
        distance_image_x / 2 - 1.0,
    )
    landing_pad_x = waypoint_position.location_x + local_x

    local_y = random.uniform(
        -distance_image_y / 2 + 1.0,
        distance_image_y / 2 - 1.0,
    )
    landing_pad_y = waypoint_position.location_y + local_y

    # Image exclusion zone
    while 6.0 < landing_pad_y % (resolution_y // pixels_per_metre) < 12.0:
        # Required for separation
        local_y = random.uniform(
            -distance_image_y / 2 + 1.0,
            distance_image_y / 2 - 1.0,
        )
        landing_pad_y = waypoint_position.location_y + local_y

    return True, location.Location(landing_pad_x, landing_pad_y)


# Better to be explicit with parameters
# pylint: disable-next=too-many-arguments
def generate_destination(drone_initial_position: location.Location,
                         boundary_bottom_left: location.Location,
                         boundary_top_right: location.Location,
                         pixels_per_metre: int,
                         resolution_x: int,
                         resolution_y: int,
                         seed: "int | None" = None) \
    -> "tuple[bool, tuple[location.Location, list[location.Location]] | None]":
    """
    Generates a waypoint and between 1 and 3 landing pads around it (inclusive).

    Waypoint cannot be within 1 image of initial position.
    Landing pads is within 0.5 image of waypoint.
    """
    if pixels_per_metre < 1:
        return False, None

    if resolution_x < 1:
        return False, None

    if resolution_y < 1:
        return False, None

    # Reproducibility
    random.seed(seed)
    __log_seed(seed)

    result, waypoint_position = __generate_waypoint(
        drone_initial_position,
        boundary_bottom_left,
        boundary_top_right,
        pixels_per_metre,
        resolution_x,
        resolution_y,
    )
    if not result:
        return False, None

    # Get Pylance to stop complaining
    assert waypoint_position is not None

    # Landing pads
    landing_pad_count = random.randint(1, 3)

    landing_pads: "list[location.Location]" = []
    for _ in range(0, landing_pad_count):
        default_landing_pad_position = location.Location(0.0, 0.0)
        landing_pad_position = default_landing_pad_position

        is_non_overlap = False
        while not is_non_overlap:
            result, landing_pad_position = __generate_landing_pad(
                waypoint_position,
                pixels_per_metre,
                resolution_x,
                resolution_y,
            )
            if not result:
                return False, None

            # Get Pylance to stop complaining
            assert landing_pad_position is not None

            # Exclusion zone with other landing pads
            is_non_overlap = True
            for landing_pad in landing_pads:
                if abs(landing_pad_position.location_x - landing_pad.location_x) < 1.0:
                    is_non_overlap = False
                    break

                if abs(landing_pad_position.location_y - landing_pad.location_y) < 1.0:
                    is_non_overlap = False
                    break

        assert landing_pad_position is not default_landing_pad_position

        landing_pads.append(landing_pad_position)

    return True, (waypoint_position, landing_pads)
