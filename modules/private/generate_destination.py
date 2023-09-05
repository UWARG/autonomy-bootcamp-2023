"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Randomly generates destination waypoint and landing pad(s).
"""
import random

from .. import location


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
    while value > exclusion_lower and value < exclusion_upper:
        value = random.uniform(lower_bound, upper_bound)

    return True, value

# Better to be explicit with parameters, extra variables required for management
# pylint: disable-next=too-many-arguments,too-many-locals
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
    # Reproducibility
    random.seed(seed)

    # Waypoint
    result, waypoint_x = __random_between_with_exclusion(
        boundary_bottom_left.location_x,
        boundary_top_right.location_x,
        drone_initial_position.location_x - resolution_x / pixels_per_metre,
        drone_initial_position.location_x + resolution_x / pixels_per_metre,
    )
    if not result:
        return False, None

    # Get Pylance to stop complaining
    assert waypoint_x is not None

    result, waypoint_y = __random_between_with_exclusion(
        boundary_bottom_left.location_y,
        boundary_top_right.location_y,
        drone_initial_position.location_y - resolution_y / pixels_per_metre,
        drone_initial_position.location_y + resolution_y / pixels_per_metre,
    )
    if not result:
        return False, None

    # Get Pylance to stop complaining
    assert waypoint_y is not None

    waypoint_position = location.Location(waypoint_x, waypoint_y)

    # Landing pads
    landing_pad_count = random.randint(1, 3)

    landing_pads = []
    for _ in range(0, landing_pad_count):
        local_x = random.uniform(
            -resolution_x / pixels_per_metre / 2,
            resolution_x / pixels_per_metre / 2,
        )
        landing_pad_x = waypoint_position.location_x + local_x

        local_y = random.uniform(
            -resolution_y / pixels_per_metre / 2,
            resolution_y / pixels_per_metre / 2,
        )
        landing_pad_y = waypoint_position.location_y + local_y

        # Image exclusion zone
        while landing_pad_y % (resolution_y // pixels_per_metre) > 6.0 \
            and landing_pad_y % (resolution_y // pixels_per_metre) < 12.0:
            # Required for separation
            local_y = random.uniform(
                -resolution_y / pixels_per_metre / 2,
                resolution_y / pixels_per_metre / 2,
            )
            landing_pad_y = waypoint_position.location_y + local_y

        landing_pad_position = location.Location(landing_pad_x, landing_pad_y)
        landing_pads.append(landing_pad_position)

    return True, (waypoint_position, landing_pads)
