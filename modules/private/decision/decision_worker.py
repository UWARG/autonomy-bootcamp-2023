"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Decision worker process.
"""

from . import base_decision
from ..utilities import queue_proxy_wrapper
from ..utilities import worker_controller


def decision_worker(
    decider: base_decision.BaseDecision,
    input_queue: queue_proxy_wrapper.QueueProxyWrapper,
    output_queue: queue_proxy_wrapper.QueueProxyWrapper,
    # Keep for consistency
    # pylint: disable-next=unused-argument
    status_queue: queue_proxy_wrapper.QueueProxyWrapper,
    controller: worker_controller.WorkerController,
):
    """
    Worker process.

    decider: Breaking the rule where the class with the run() method is not supposed to be passed
        since there are several options.

    input_queue and output_queue are data queues.
    status_queue is how this worker process communicates to the main process.
    controller is how the main process communicates to this worker process.
    """
    while not controller.is_exit_requested():
        controller.check_pause()

        input_data = input_queue.queue.get()
        if input_data is None:
            break

        report, landing_pad_locations, _ = input_data

        try:
            command = decider.run(report, landing_pad_locations)
        # Bootcamper can throw any exception
        # pylint: disable-next=broad-exception-caught
        except Exception:
            print("WORKER ERROR: BaseDecision.run() exception")
            status_queue.queue.put(report)
            return

        output_queue.queue.put(command)
