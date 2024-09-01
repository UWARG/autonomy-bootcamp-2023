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


def run_simulator(
    command: commands.Command, drone: drone_state.DroneState, renderer: map_render.MapRender
) -> "tuple[bool, tuple[drone_report.DroneReport, np.ndarray] | None]":
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


def simulation_worker(
    time_step_size: float,
    drone_initial_position: location.Location,
    boundary_bottom_left: location.Location,
    boundary_top_right: location.Location,
    acceptance_radius: float,
    pixels_per_metre: int,
    image_resolution_x: int,
    image_resolution_y: int,
    map_image_directory: pathlib.Path,
    landing_pad_image_directory: pathlib.Path,
    landing_pad_locations: "list[location.Location]",
    input_queue: queue_proxy_wrapper.QueueProxyWrapper,
    output_queue: queue_proxy_wrapper.QueueProxyWrapper,
    status_queue: queue_proxy_wrapper.QueueProxyWrapper,
    controller: worker_controller.WorkerController,
) -> None:
    """
    Worker process.

    input_queue and output_queue are data queues.
    status_queue is how this worker process communicates to the main process.
    controller is how the main process communicates to this worker process.
    """
    previous = (
        drone_report.DroneReport(
            drone_status.DroneStatus.HALTED,
            drone_initial_position,
            drone_initial_position,
        ),
        np.zeros((image_resolution_y, image_resolution_x, 3)),
    )

    result, drone = drone_state.DroneState.create(
        time_step_size,
        drone_initial_position,
        boundary_bottom_left,
        boundary_top_right,
        acceptance_radius,
    )
    if not result:
        print("WORKER ERROR: Could not create drone state")
        status_queue.queue.put(previous[0])
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
        status_queue.queue.put(previous[0])
        print("WORKER ERROR: Could not create map renderer")
        return

    # Get Pylance to stop complaining
    assert renderer is not None

    # Run once
    input_data = commands.Command.create_null_command()
    result, current = run_simulator(input_data, drone, renderer)
    if not result:
        print("WORKER ERROR: Simulation step failed")
        current = previous

    # Get Pylance to stop complaining
    assert current is not None

    output_data = (current[0], [], current[1])

    output_queue.queue.put(output_data)

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

        # Get Pylance to stop complaining
        assert current is not None

        output_data = (current[0], [], current[1])

        output_queue.queue.put(output_data)

        previous = current

        # Request main to request exit
        if previous[0].status == drone_status.DroneStatus.LANDED:
            status_queue.queue.put(previous[0])
            print("WORKER: Drone has landed, exiting")
            return

        time.sleep(time_step_size)
