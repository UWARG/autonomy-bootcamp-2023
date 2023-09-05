"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Detect landing pad worker process.
"""
import pathlib

from .utilities import queue_proxy_wrapper
from .utilities import worker_controller
from ..bootcamp import detect_landing_pad


def detect_landing_pad_worker(model_directory: pathlib.Path,
                              input_queue: queue_proxy_wrapper.QueueProxyWrapper,
                              output_queue: queue_proxy_wrapper.QueueProxyWrapper,
                              status_queue: queue_proxy_wrapper.QueueProxyWrapper,
                              controller: worker_controller.WorkerController):
    """
    Worker process.

    input_queue and output_queue are data queues.
    status_queue is how this worker process communicates to the main process.
    controller is how the main process communicates to this worker process.
    """
    result, detector = detect_landing_pad.DetectLandingPad.create(model_directory)
    if not result:
        print("WORKER ERROR: Could not create landing pad detector")
        status_queue.queue.put(-1)
        return

    # Get Pylance to stop complaining
    assert detector is not None

    while not controller.is_exit_requested():
        controller.check_pause()

        input_data = input_queue.queue.get()
        if input_data is None:
            break

        report, _, camera_image = input_data

        try:
            bounding_boxes, annotated_image = detector.run(camera_image)
        # Bootcamper can throw any exception
        # pylint: disable-next=broad-exception-caught
        except Exception:
            print("WORKER ERROR: DetectLandingPad.run() exception")
            bounding_boxes = [], annotated_image = camera_image

        output_data = (report, bounding_boxes, annotated_image)

        output_queue.queue.put(output_data)
