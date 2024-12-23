"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Common implementation of runner for main.
"""

import multiprocessing as mp
import pathlib
import time

from . import decision_factory
from .... import location
from ....private import detect_landing_pad_worker
from ....private import generate_destination
from ....private.decision import decision_worker
from ....private.display import display_worker
from ....private.geolocation import geolocation_worker
from ....private.simulation import simulation_worker
from ....private.utilities import queue_proxy_wrapper
from ....private.utilities import worker_controller
from ....private.utilities import worker_manager


QUEUE_MAX_SIZE = 1
TIMEOUT = 1000  # seconds
LOG_FILE_DIRECTORY = pathlib.Path("log")
TIME_WAIT_BEFORE_EXIT = 5  # seconds

DRONE_INITIAL_POSITION = location.Location(0.0, 0.0)
BOUNDARY_BOTTOM_LEFT = location.Location(-60.0, -60.0)
BOUNDARY_TOP_RIGHT = location.Location(60.0, 60.0)
ACCEPTANCE_RADIUS = 0.1  # metres
PIXELS_PER_METRE = 60
IMAGE_RESOLUTION_X = 1200
IMAGE_RESOLUTION_Y = 900
MAP_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/world")
LANDING_PAD_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/assets")

MODEL_DIRECTORY_PATH = pathlib.Path("models")


def runner(
    decision_enum: decision_factory.DecisionEnum,
    time_step_size: float,
    display_scale: float,
    seed: int,
) -> int:
    """
    main's implementation.
    """
    # Setup
    controller = worker_controller.WorkerController()

    mp_manager = mp.Manager()

    # Data queues
    simulation_to_detect_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    detect_to_geolocation_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    geolocation_to_display_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    display_to_decision_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    decision_to_simulation_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )

    # Status queues
    worker_status_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
    )

    # Variables
    result, data = generate_destination.generate_destination(
        DRONE_INITIAL_POSITION,
        BOUNDARY_BOTTOM_LEFT,
        BOUNDARY_TOP_RIGHT,
        PIXELS_PER_METRE,
        IMAGE_RESOLUTION_X,
        IMAGE_RESOLUTION_Y,
        seed,
    )
    if not result:
        print("ERROR: Could not generate waypoint and landing pads")
        return -1

    # Get Pylance to stop complaining
    assert data is not None

    waypoint, landing_pad_locations = data

    # Override in the example to show landing pads
    if decision_enum == decision_factory.DecisionEnum.EXAMPLE:
        landing_pad_locations = [
            location.Location(-40.0, 0.5),
        ]

    # Override in the simple waypoint as randomized landing pads are not needed
    if decision_enum == decision_factory.DecisionEnum.SIMPLE_WAYPOINT:
        landing_pad_locations = [
            waypoint,
        ]

    # Add landing pad at initial position
    landing_pad_locations.append(DRONE_INITIAL_POSITION)

    decider = decision_factory.create_decision(decision_enum, waypoint, ACCEPTANCE_RADIUS)

    # Managers
    simulation_manager = worker_manager.WorkerManager()
    simulation_manager.create_workers(
        1,
        simulation_worker.simulation_worker,
        (
            time_step_size,
            DRONE_INITIAL_POSITION,
            BOUNDARY_BOTTOM_LEFT,
            BOUNDARY_TOP_RIGHT,
            ACCEPTANCE_RADIUS,
            PIXELS_PER_METRE,
            IMAGE_RESOLUTION_X,
            IMAGE_RESOLUTION_Y,
            MAP_IMAGES_PATH,
            LANDING_PAD_IMAGES_PATH,
            landing_pad_locations,
            decision_to_simulation_queue,
            simulation_to_detect_queue,
            worker_status_queue,
            controller,
        ),
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
            worker_status_queue,
            controller,
        ),
    )

    display_manager = worker_manager.WorkerManager()
    display_manager.create_workers(
        1,
        display_worker.display_worker,
        (
            display_scale,
            seed,
            geolocation_to_display_queue,
            display_to_decision_queue,
            worker_status_queue,
            controller,
        ),
    )

    decision_manager = worker_manager.WorkerManager()
    decision_manager.create_workers(
        1,
        decision_worker.decision_worker,
        (
            decider,
            display_to_decision_queue,
            decision_to_simulation_queue,
            worker_status_queue,
            controller,
        ),
    )

    simulation_manager.start_workers()
    detect_landing_pad_manager.start_workers()
    geolocation_manager.start_workers()
    display_manager.start_workers()
    decision_manager.start_workers()

    report = worker_status_queue.queue.get(timeout=TIMEOUT)

    # Log results
    results_text = f"{report}\nSeed: {seed}\nWaypoint: {waypoint}\n"
    for landing_pad_location in landing_pad_locations:
        results_text += f"Landing pad: {landing_pad_location}\n"

    file_name = f"{int(time.time())}_results.txt"
    file_path = pathlib.Path(LOG_FILE_DIRECTORY, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(results_text)

    print("Logged results")

    time.sleep(TIME_WAIT_BEFORE_EXIT)

    print("main is requesting exit")
    controller.request_exit()

    # Teardown
    print("Start teardown")

    simulation_to_detect_queue.fill_and_drain_queue()
    detect_to_geolocation_queue.fill_and_drain_queue()
    geolocation_to_display_queue.fill_and_drain_queue()
    display_to_decision_queue.fill_and_drain_queue()
    decision_to_simulation_queue.fill_and_drain_queue()

    worker_status_queue.fill_and_drain_queue()

    simulation_manager.join_workers()
    detect_landing_pad_manager.join_workers()
    geolocation_manager.join_workers()
    display_manager.join_workers()
    decision_manager.join_workers()

    return 0
