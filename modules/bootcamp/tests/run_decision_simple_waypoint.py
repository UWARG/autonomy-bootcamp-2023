"""
BOOTCAMPERS TO COMPLETE.

Test decision simple waypoint.

You can change the timestep, display scale, and seed, if you wish.
Do not modify anything else.
"""
import multiprocessing as mp
import pathlib
import time

from modules import location
from modules.bootcamp import decision_simple_waypoint
from modules.private import generate_destination
from modules.private.decision import decision_worker
from modules.private.display import display_worker
from modules.private.simulation import simulation_worker
from modules.private.utilities import queue_proxy_wrapper
from modules.private.utilities import worker_controller
from modules.private.utilities import worker_manager


QUEUE_MAX_SIZE = 1
TIMEOUT = 1000  # seconds
LOG_FILE_DIRECTORY = pathlib.Path("log")
TIME_WAIT_BEFORE_EXIT = 5  # seconds

# ============
# ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# ============

# From the value you determined was good in run_decision_example.py
# You can probably divide it by 10 or so since ML inference isn't running
# Increase the step size if your computer is lagging
# Larger step size is smaller FPS
TIME_STEP_SIZE = 0.1  # seconds

# OpenCV ignores your display settings,
# so if the window is too small or too large,
# change this value (between 0.0 and 1.0)
DISPLAY_SCALE = 0.7

# Seed for randomly generating the waypoint and landing pad
# Change to a constant for reproducibility (e.g. debugging)
# Change back to = time.time_ns() to test robustness
SEED = time.time_ns()

# ============
# ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# ============

DRONE_INITIAL_POSITION = location.Location(0.0, 0.0)
BOUNDARY_BOTTOM_LEFT = location.Location(-60.0, -60.0)
BOUNDARY_TOP_RIGHT = location.Location(60.0, 60.0)
ACCEPTANCE_RADIUS = 0.1  # metres
PIXELS_PER_METRE = 60
IMAGE_RESOLUTION_X = 1200
IMAGE_RESOLUTION_Y = 900
MAP_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/world")
LANDING_PAD_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/assets")


# Extra variables required for management, extra statements required for management
# pylint: disable-next=too-many-locals,too-many-statements
def main() -> int:
    """
    main.
    """
    # Setup
    controller = worker_controller.WorkerController()

    mp_manager = mp.Manager()

    # Data queues
    simulation_to_display_queue = queue_proxy_wrapper.QueueProxyWrapper(
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
        SEED,
    )
    if not result:
        print("ERROR: Could not generate waypoint and landing pads")
        return -1

    # Get Pylance to stop complaining
    assert data is not None

    waypoint, landing_pad_locations = data

    # Override as randomized landing pads are not needed here
    landing_pad_locations = [
        waypoint,
        DRONE_INITIAL_POSITION,
    ]

    decider = decision_simple_waypoint.DecisionSimpleWaypoint(waypoint, ACCEPTANCE_RADIUS)

    # Managers
    simulation_manager = worker_manager.WorkerManager()
    simulation_manager.create_workers(
        1,
        simulation_worker.simulation_worker,
        (
            TIME_STEP_SIZE,
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
            simulation_to_display_queue,
            worker_status_queue,
            controller,
        ),
    )

    display_manager = worker_manager.WorkerManager()
    display_manager.create_workers(
        1,
        display_worker.display_worker,
        (
            DISPLAY_SCALE,
            SEED,
            simulation_to_display_queue,
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
    display_manager.start_workers()
    decision_manager.start_workers()

    report = worker_status_queue.queue.get(timeout=TIMEOUT)

    # Log results
    results_text = \
        str(report) + "\n"\
        + "Seed: " + str(SEED) + "\n"\
        + "Waypoint: " + str(waypoint) + "\n"\

    for landing_pad_location in landing_pad_locations:
        results_text += "Landing pad: " + str(landing_pad_location) + "\n"

    file_name = str(int(time.time())) + "_results.txt"
    file_path = pathlib.Path(LOG_FILE_DIRECTORY, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(results_text)

    print("Logged results")

    time.sleep(TIME_WAIT_BEFORE_EXIT)

    print("main is requesting exit")
    controller.request_exit()

    # Teardown
    print("Start teardown")

    simulation_to_display_queue.fill_and_drain_queue()
    display_to_decision_queue.fill_and_drain_queue()
    decision_to_simulation_queue.fill_and_drain_queue()

    worker_status_queue.fill_and_drain_queue()

    simulation_manager.join_workers()
    display_manager.join_workers()
    decision_manager.join_workers()

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    status = main()
    if status < 0:
        print("ERROR: Status code: " + str(status))

    print("Done!")
