"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Simulation worker process.
"""
import pathlib
import time

import numpy as np

from .drone import drone_state
from .mapping import map_render
from ..utilities import queue_proxy_wrapper
from ..utilities import worker_controller
from ... import commands
from ... import drone_report
from ... import drone_status
from ... import location


TIME_STEP_SIZE = 0.01  # seconds


def run_simulator(command: commands.Command,
                  drone: drone_state.DroneState,
                  renderer: map_render.MapRender) \
    -> "tuple[bool, tuple[drone_report.DroneReport, np.ndarray] | None]":
    """
    Wrapper.
    """
    report, _ = drone.run(command)
    result, camera_image = renderer.run(report.position)
    if not result:
        return False, None

    # Get Pylance to stop complaining
    assert camera_image is not None

    return True, (report, camera_image)


# Extra parameters required for worker communication, extra variables required for management
# pylint: disable-next=too-many-arguments,too-many-locals
def simulation_worker(drone_initial_position: location.Location,
                      boundary_top_left: location.Location,
                      boundary_bottom_right: location.Location,
                      pixels_per_metre: int,
                      image_resolution_x: int,
                      image_resolution_y: int,
                      map_image_directory: pathlib.Path,
                      landing_pad_image_directory: pathlib.Path,
                      landing_pad_locations: "list[location.Location]",
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
    result, drone = drone_state.DroneState.create(
        TIME_STEP_SIZE,
        drone_initial_position,
        boundary_top_left,
        boundary_bottom_right,
    )
    if not result:
        print("WORKER ERROR: Could not create drone state")
        status_queue.queue.put(-1)
        return

    # Get Pylance to stop complaining
    assert drone is not None

    result, renderer = map_render.MapRender.create(
        pixels_per_metre,
        image_resolution_x,
        image_resolution_y,
        map_image_directory,
        landing_pad_image_directory,
        landing_pad_locations,
    )
    if not result:
        status_queue.queue.put(-1)
        print("WORKER ERROR: Could not create map renderer")
        return

    # Get Pylance to stop complaining
    assert renderer is not None

    previous = (
        drone_report.DroneReport(
            drone_status.DroneStatus.HALTED,
            drone_initial_position,
            drone_initial_position,
        ),
        np.zeros((image_resolution_y, image_resolution_x, 3)),
    )

    # Run once
    input_data = commands.Command.create_null_command()
    result, current = run_simulator(input_data, drone, renderer)
    if not result:
        print("WORKER ERROR: Simulation step failed")
        current = previous

    output_queue.queue.put(current)

    previous = current

    while not controller.is_exit_requested():
        controller.check_pause()

        input_data = input_queue.queue.get()
        if input_data is None:
            break

        result, current = run_simulator(input_data, drone, renderer)
        if not result:
            print("WORKER ERROR: Simulation step failed")
            current = previous

        output_queue.queue.put(current)

        previous = current

        time.sleep(TIME_STEP_SIZE)
