"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test geolocation.
"""

import numpy as np
import pytest

from modules import bounding_box
from modules import drone_report
from modules import drone_status
from modules import location
from modules.private.geolocation import geolocation


PIXELS_PER_METRE = 60
IMAGE_RESOLUTION_X = 1200
IMAGE_RESOLUTION_Y = 900


@pytest.fixture()
def locator():
    """
    Construct Geolocation.
    """
    _, geolocator = geolocation.Geolocation.create(
        PIXELS_PER_METRE,
        IMAGE_RESOLUTION_X,
        IMAGE_RESOLUTION_Y,
    )
    assert geolocator is not None

    return geolocator


@pytest.fixture()
def report():
    """
    Drone report.
    """
    drone = drone_report.DroneReport(
        drone_status.DroneStatus.HALTED,
        location.Location(1.0, 1.0),
        location.Location(1.0, 1.0),
    )
    return drone


# Pytest requires the parameter and fixture names to be identical
# pylint: disable=redefined-outer-name


def test_input_empty(locator: geolocation.Geolocation, report: drone_report.DroneReport):
    """
    No bounding boxes.
    """
    # Setup
    bounding_boxes = []
    expected = []

    # Run
    actual = locator.run(report, bounding_boxes)

    # Test
    assert actual == expected


def test_input_1(locator: geolocation.Geolocation, report: drone_report.DroneReport):
    """
    1 bounding box.
    """
    # Setup
    possibly_bounding_boxes = [
        bounding_box.BoundingBox.create(np.array([540.0, 510.0, 540.0, 510.0]))[1],
    ]
    bounding_boxes = []
    for box in possibly_bounding_boxes:
        assert box is not None
        bounding_boxes.append(box)

    expected = [
        location.Location(0.0, 0.0),
    ]

    # Run
    actual = locator.run(report, bounding_boxes)

    # Test
    assert actual == expected


def test_input_2(locator: geolocation.Geolocation, report: drone_report.DroneReport):
    """
    2 bounding boxes.
    """
    # Setup
    possibly_bounding_boxes = [
        bounding_box.BoundingBox.create(np.array([480.0, 450.0, 480.0, 450.0]))[1],
        bounding_box.BoundingBox.create(np.array([600.0, 570.0, 600.0, 570.0]))[1],
    ]
    bounding_boxes = []
    for box in possibly_bounding_boxes:
        assert box is not None
        bounding_boxes.append(box)

    expected = [
        location.Location(-1.0, 1.0),
        location.Location(1.0, -1.0),
    ]

    # Run
    actual = locator.run(report, bounding_boxes)

    # Test
    assert actual == expected
