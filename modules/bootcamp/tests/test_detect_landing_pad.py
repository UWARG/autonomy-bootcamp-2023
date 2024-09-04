"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Unit tests.
"""

import pathlib

import cv2
import numpy as np
import pytest

from modules import bounding_box
from modules.bootcamp import detect_landing_pad


MODEL_DIRECTORY_PATH = pathlib.Path("models")
INPUT_IMAGES_PATH = pathlib.Path("modules/bootcamp/tests")
OUTPUT_IMAGES_PATH = pathlib.Path("modules/bootcamp/tests/log")

BOUNDING_BOX_TOLERANCE = 1.0  # pixels


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture()
def detector() -> detect_landing_pad.DetectLandingPad:  # type: ignore
    """
    Construct DetectLandingPad.
    """
    _, detection = detect_landing_pad.DetectLandingPad.create(MODEL_DIRECTORY_PATH)
    assert detection is not None

    # Hang output directory creation on this as well
    OUTPUT_IMAGES_PATH.mkdir(parents=True, exist_ok=True)

    yield detection  # type: ignore


def test_single_landing_pad(detector: detect_landing_pad.DetectLandingPad) -> None:
    """
    1 landing pad.
    """
    # Setup
    image_name = "map_1_landing_pad.png"
    input_path = pathlib.Path(INPUT_IMAGES_PATH, image_name)
    assert input_path.exists()
    output_path = pathlib.Path(OUTPUT_IMAGES_PATH, image_name)

    input_image = cv2.imread(str(input_path))
    assert input_image is not None

    expected_boxes = [
        bounding_box.BoundingBox.create(np.array([846.0, 604.0, 896.0, 655.0]))[1],
    ]
    for box in expected_boxes:
        assert box is not None

    # Run
    actual_boxes, output_image = detector.run(input_image)

    # Test
    assert len(actual_boxes) == 1
    for i, actual_box in enumerate(actual_boxes):
        expected = expected_boxes[i]
        assert expected is not None
        assert bounding_box.BoundingBox.is_close(actual_box, expected, BOUNDING_BOX_TOLERANCE)

    cv2.imwrite(str(output_path), output_image)


def test_double_landing_pad(detector: detect_landing_pad.DetectLandingPad) -> None:
    """
    2 landing pads.
    """
    # Setup
    image_name = "map_2_landing_pad.png"
    input_path = pathlib.Path(INPUT_IMAGES_PATH, image_name)
    assert input_path.exists()
    output_path = pathlib.Path(OUTPUT_IMAGES_PATH, image_name)

    input_image = cv2.imread(str(input_path))
    assert input_image is not None

    expected_boxes = [
        bounding_box.BoundingBox.create(np.array([845.8, 604.5, 896.1, 654.9]))[1],
        bounding_box.BoundingBox.create(np.array([513.2, 33.9, 562.5, 85.2]))[1],
    ]

    for box in expected_boxes:
        assert box is not None

    # Run
    actual_boxes, output_image = detector.run(input_image)

    # Test
    assert len(actual_boxes) == 2
    for i, actual_box in enumerate(actual_boxes):
        expected = expected_boxes[i]
        assert expected is not None
        assert bounding_box.BoundingBox.is_close(actual_box, expected, BOUNDING_BOX_TOLERANCE)

    cv2.imwrite(str(output_path), output_image)


def test_zero_landing_pad(detector: detect_landing_pad.DetectLandingPad) -> None:
    """
    0 landing pads.
    """
    # Setup
    image_name = "map_0_landing_pad.png"
    input_path = pathlib.Path(INPUT_IMAGES_PATH, image_name)
    assert input_path.exists()
    output_path = pathlib.Path(OUTPUT_IMAGES_PATH, image_name)

    input_image = cv2.imread(str(input_path))
    assert input_image is not None

    # Run
    actual_boxes, output_image = detector.run(input_image)

    # Test
    assert len(actual_boxes) == 0

    cv2.imwrite(str(output_path), output_image)
