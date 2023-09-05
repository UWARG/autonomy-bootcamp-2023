"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test geolocation worker.
"""
import multiprocessing as mp

import numpy as np

from modules import bounding_box
from modules import drone_report
from modules import drone_status
from modules import location
from modules.private.geolocation import geolocation_worker
from modules.private.utilities import queue_proxy_wrapper
from modules.private.utilities import worker_controller
from modules.private.utilities import worker_manager


QUEUE_MAX_SIZE = 1

PIXELS_PER_METRE = 60
IMAGE_RESOLUTION_X = 1200
IMAGE_RESOLUTION_Y = 900


# Extra variables required for management
# pylint: disable-next=too-many-locals
def main() -> int:
    """
    main.
    """
    # Setup
    controller = worker_controller.WorkerController()

    mp_manager = mp.Manager()

    detect_to_geolocation_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    geolocation_to_display_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )

    geolocation_worker_status_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
    )

    geolocation_manager = worker_manager.WorkerManager()
    geolocation_manager.create_workers(
        1,
        geolocation_worker.geolocation_worker,
        (
            PIXELS_PER_METRE,
            IMAGE_RESOLUTION_X,
            IMAGE_RESOLUTION_Y,
            detect_to_geolocation_queue,
            geolocation_to_display_queue,
            geolocation_worker_status_queue,
            controller,
        ),
    )

    geolocation_manager.start_workers()

    bounding_boxes_list = [
        [],
        [
            bounding_box.BoundingBox.create(np.array([540.0, 510.0, 540.0, 510.0]))[1]
        ],
        [
            bounding_box.BoundingBox.create(np.array([480.0, 450.0, 480.0, 450.0]))[1],
            bounding_box.BoundingBox.create(np.array([600.0, 570.0, 600.0, 570.0]))[1],
        ],
    ]

    drone_position = location.Location(1.0, 1.0)
    input_report = drone_report.DroneReport(
        drone_status.DroneStatus.HALTED,
        drone_position,
        drone_position,
    )

    input_image = np.zeros((IMAGE_RESOLUTION_Y, IMAGE_RESOLUTION_X, 3))

    for i, bounding_boxes in enumerate(bounding_boxes_list):
        # Run
        input_data = (input_report, bounding_boxes, input_image)
        detect_to_geolocation_queue.queue.put(input_data)

        # Test
        output_data: "tuple[drone_report.DroneReport, list[location.Location], np.ndarray]" \
            = geolocation_to_display_queue.queue.get()
        report, positions, annotated_image = output_data

        assert report == input_report
        assert len(positions) == i
        np.testing.assert_equal(annotated_image, input_image)

    controller.request_exit()

    # Teardown
    detect_to_geolocation_queue.fill_and_drain_queue()
    geolocation_to_display_queue.fill_and_drain_queue()

    geolocation_worker_status_queue.fill_and_drain_queue()

    geolocation_manager.join_workers()

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    status = main()
    if status < 0:
        print("ERROR: Status code: " + str(status))

    print("Done!")
