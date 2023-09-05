"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test display.
"""
import math
import time

import cv2

from modules import drone_report
from modules import drone_status
from modules import location
from modules.private.display import display


DISPLAY_SCALE = 0.8

DELAY = 0.01  # seconds


if __name__ == "__main__":
    _, displayer = display.Display.create(DISPLAY_SCALE)
    assert displayer is not None

    image = cv2.imread("modules/private/simulation/mapping/world/default.png")
    assert image is not None

    report = drone_report.DroneReport(
        drone_status.DroneStatus.HALTED,
        location.Location(math.sqrt(2), -10 * math.sqrt(3)),
        location.Location(-100 * math.sqrt(5), math.pi),
    )
    for _ in range(0, 100):
        _ = displayer.run(report, image)
        time.sleep(DELAY)

    report = drone_report.DroneReport(
        drone_status.DroneStatus.MOVING,
        location.Location(math.sqrt(2), -10 * math.sqrt(3)),
        location.Location(-100 * math.sqrt(5), math.pi),
    )
    for _ in range(0, 100):
        _ = displayer.run(report, image)
        time.sleep(DELAY)

    report = drone_report.DroneReport(
        drone_status.DroneStatus.LANDED,
        location.Location(math.sqrt(2), -10 * math.sqrt(3)),
        location.Location(-100 * math.sqrt(5), math.pi),
    )
    for _ in range(0, 100):
        _ = displayer.run(report, image)
        time.sleep(DELAY)

    print("Done!")
