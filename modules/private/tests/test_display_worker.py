"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test display worker.
"""

import math
import multiprocessing as mp
import pathlib
import time

import cv2
import numpy as np

from modules import drone_report
from modules import drone_status
from modules import location
from modules.private.display import display_worker
from modules.private.utilities import queue_proxy_wrapper
from modules.private.utilities import worker_controller
from modules.private.utilities import worker_manager


QUEUE_MAX_SIZE = 1

DISPLAY_SCALE = 0.8
SEED = time.time_ns()
IMAGE_PATH = pathlib.Path("modules/private/simulation/mapping/world/default.png")

DELAY = 0.01  # seconds


# Extra variables required for management
# pylint: disable-next=too-many-locals
def main() -> int:
    """
    main.
    """
    # Setup
    controller = worker_controller.WorkerController()

    mp_manager = mp.Manager()

    input_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    display_to_decision_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )

    worker_status_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
    )

    display_manager = worker_manager.WorkerManager()
    display_manager.create_workers(
        1,
        display_worker.display_worker,
        (
            DISPLAY_SCALE,
            SEED,
            input_queue,
            display_to_decision_queue,
            worker_status_queue,
            controller,
        ),
    )

    display_manager.start_workers()

    input_list = []

    assert IMAGE_PATH.exists()

    # Pylint has issues with OpenCV
    # pylint: disable-next=no-member
    input_image = cv2.imread(str(IMAGE_PATH))
    assert input_image is not None

    input_report = drone_report.DroneReport(
        drone_status.DroneStatus.HALTED,
        location.Location(math.sqrt(2), -10 * math.sqrt(3)),
        location.Location(-100 * math.sqrt(5), math.pi),
    )
    for _ in range(0, 100):
        # Run
        input_data = (input_report, input_list, input_image)
        input_queue.queue.put(input_data)

        # Test
        output_data: "tuple[drone_report.DroneReport, list, np.ndarray]" = (
            display_to_decision_queue.queue.get()
        )
        report, output_list, output_image = output_data

        assert report == input_report
        assert output_list == input_list
        assert output_image.shape == input_image.shape

        time.sleep(DELAY)

    input_report = drone_report.DroneReport(
        drone_status.DroneStatus.MOVING,
        location.Location(math.sqrt(2), -10 * math.sqrt(3)),
        location.Location(-100 * math.sqrt(5), math.pi),
    )
    for _ in range(0, 100):
        # Run
        input_data = (input_report, input_list, input_image)
        input_queue.queue.put(input_data)

        # Test
        output_data: "tuple[drone_report.DroneReport, list, np.ndarray]" = (
            display_to_decision_queue.queue.get()
        )
        report, output_list, output_image = output_data

        assert report == input_report
        assert output_list == input_list
        assert output_image.shape == input_image.shape

        time.sleep(DELAY)

    input_report = drone_report.DroneReport(
        drone_status.DroneStatus.LANDED,
        location.Location(math.sqrt(2), -10 * math.sqrt(3)),
        location.Location(-100 * math.sqrt(5), math.pi),
    )
    for _ in range(0, 100):
        # Run
        input_data = (input_report, input_list, input_image)
        input_queue.queue.put(input_data)

        # Test
        output_data: "tuple[drone_report.DroneReport, list, np.ndarray]" = (
            display_to_decision_queue.queue.get()
        )
        report, output_list, output_image = output_data

        assert report == input_report
        assert output_list == input_list
        assert output_image.shape == input_image.shape

        time.sleep(DELAY)

    controller.request_exit()

    # Teardown
    input_queue.fill_and_drain_queue()
    display_to_decision_queue.fill_and_drain_queue()

    worker_status_queue.fill_and_drain_queue()

    display_manager.join_workers()

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    status = main()
    if status < 0:
        print("ERROR: Status code: " + str(status))

    print("Done!")
