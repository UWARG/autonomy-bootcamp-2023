"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Display worker process.
"""

from . import display
from ..utilities import queue_proxy_wrapper
from ..utilities import worker_controller
from ... import drone_report
from ... import drone_status
from ... import location


# Extra parameters required for worker communication
# pylint: disable-next=too-many-arguments
def display_worker(
    display_scale: float,
    seed: int,
    input_queue: queue_proxy_wrapper.QueueProxyWrapper,
    output_queue: queue_proxy_wrapper.QueueProxyWrapper,
    status_queue: queue_proxy_wrapper.QueueProxyWrapper,
    controller: worker_controller.WorkerController,
):
    """
    Worker process.

    input_queue and output_queue are data queues.
    status_queue is how this worker process communicates to the main process.
    controller is how the main process communicates to this worker process.
    """
    report = drone_report.DroneReport(
        drone_status.DroneStatus.HALTED,
        location.Location(0.0, 0.0),
        location.Location(0.0, 0.0),
    )

    result, displayer = display.Display.create(display_scale, seed)
    if not result:
        print("WORKER ERROR: Could not create displayer")
        status_queue.queue.put(report)
        return

    # Get Pylance to stop complaining
    assert displayer is not None

    while not controller.is_exit_requested():
        controller.check_pause()

        input_data = input_queue.queue.get()
        if input_data is None:
            break

        report, landing_pad_positions, image = input_data

        result = displayer.run(report, image)
        if not result:
            print("WORKER ERROR: Could not display image")

        output_data = (report, landing_pad_positions, image)

        output_queue.queue.put(output_data)
