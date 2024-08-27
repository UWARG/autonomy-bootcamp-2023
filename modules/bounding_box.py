"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Bounding box for detected landing pad.
"""

import numpy as np


# Basically a struct
# pylint: disable=too-few-public-methods
class BoundingBox:
    """
    A detected landing pad in image space.
    """

    __create_key = object()

    @classmethod
    def create(cls, bounds: np.ndarray) -> "tuple[bool, BoundingBox | None]":
        """
        bounds are of form x1, y1, x2, y2 .
        """
        # Check every element in bounds is >= 0.0
        if bounds.shape != (4,) or not np.greater_equal(bounds, 0.0).all():
            return False, None

        # n1 <= n2
        if bounds[0] > bounds[2] or bounds[1] > bounds[3]:
            return False, None

        return True, BoundingBox(cls.__create_key, bounds)

    def __init__(self, class_private_create_key: object, bounds: np.ndarray) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is BoundingBox.__create_key, "Use create() method"

        # Mixing letters and numbers confuses Pylint
        # pylint: disable=invalid-name
        self.x1 = bounds[0]
        self.y1 = bounds[1]
        self.x2 = bounds[2]
        self.y2 = bounds[3]
        # pylint: enable=invalid-name

    @staticmethod
    def __is_within_tolerance(number_a: float, number_b: float, tolerance: float) -> bool:
        """
        Checks if 2 numbers are within a tolerance.
        """
        return abs(number_a - number_b) <= tolerance

    @staticmethod
    def is_close(
        bounding_box_1: "BoundingBox", bounding_box_2: "BoundingBox", tolerance: float
    ) -> bool:
        """
        Whether the bounds are close enough.
        """
        if not BoundingBox.__is_within_tolerance(bounding_box_1.x1, bounding_box_2.x1, tolerance):
            return False

        if not BoundingBox.__is_within_tolerance(bounding_box_1.y1, bounding_box_2.y1, tolerance):
            return False

        if not BoundingBox.__is_within_tolerance(bounding_box_1.x2, bounding_box_2.x2, tolerance):
            return False

        if not BoundingBox.__is_within_tolerance(bounding_box_1.y2, bounding_box_2.y2, tolerance):
            return False

        return True

    def get_centre(self) -> "tuple[float, float]":
        """
        Gets the xy centre of the bounding box.
        """
        centre_x = (self.x1 + self.x2) / 2
        centre_y = (self.y1 + self.y2) / 2
        return centre_x, centre_y

    def __repr__(self) -> str:
        """
        To string.
        """
        representation = "Bounding box: " + str((self.x1, self.y1)) + "," + str((self.x2, self.y2))

        return representation
