"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test landing pad detection worker.
"""

import multiprocessing as mp
import pathlib

import cv2
import numpy as np

from modules import bounding_box
from modules import drone_report
from modules import drone_status
from modules import location
from modules.private import detect_landing_pad_worker
from modules.private.utilities import queue_proxy_wrapper
from modules.private.utilities import worker_controller
from modules.private.utilities import worker_manager


QUEUE_MAX_SIZE = 1

MODEL_DIRECTORY_PATH = pathlib.Path("models")
INPUT_IMAGES_PATH = pathlib.Path("modules/bootcamp/tests")
OUTPUT_IMAGES_PATH = pathlib.Path("modules/private/tests/log")


def main() -> int:
    """
    main.
    """
    # Setup
    controller = worker_controller.WorkerController()

    mp_manager = mp.Manager()

    simulation_to_detect_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    detect_to_geolocation_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )

    worker_status_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
    )

    detect_landing_pad_manager = worker_manager.WorkerManager()
    detect_landing_pad_manager.create_workers(
        1,
        detect_landing_pad_worker.detect_landing_pad_worker,
        (
            MODEL_DIRECTORY_PATH,
            simulation_to_detect_queue,
            detect_to_geolocation_queue,
            worker_status_queue,
            controller,
        ),
    )

    detect_landing_pad_manager.start_workers()

    camera_images = []
    for i in range(0, 3):
        input_image_path = pathlib.Path(INPUT_IMAGES_PATH, f"map_{i}_landing_pad.png")
        assert input_image_path.exists()
        camera_image = cv2.imread(str(input_image_path))
        assert camera_image is not None
        camera_images.append(camera_image)

    drone_position = location.Location(0.0, 0.0)
    input_report = drone_report.DroneReport(
        drone_status.DroneStatus.HALTED,
        drone_position,
        drone_position,
    )

    OUTPUT_IMAGES_PATH.mkdir(parents=True, exist_ok=True)

    for i, camera_image in enumerate(camera_images):
        # Run
        input_data = (input_report, [], camera_image)
        simulation_to_detect_queue.queue.put(input_data)

        # Test
        output_data: (
            "tuple[drone_report.DroneReport, list[bounding_box.BoundingBox], np.ndarray]"
        ) = detect_to_geolocation_queue.queue.get()
        report, bounding_boxes, annotated_image = output_data

        assert report == input_report
        assert len(bounding_boxes) == i
        output_image_path = pathlib.PurePosixPath(OUTPUT_IMAGES_PATH, f"map_{i}_landing_pad.png")
        cv2.imwrite(str(output_image_path), annotated_image)

    controller.request_exit()

    # Teardown
    simulation_to_detect_queue.fill_and_drain_queue()
    detect_to_geolocation_queue.fill_and_drain_queue()

    worker_status_queue.fill_and_drain_queue()

    detect_landing_pad_manager.join_workers()

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
