"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test drone state simulation with a figure 8.
"""

import multiprocessing as mp
import pathlib

import cv2
import numpy as np

from modules import commands
from modules import drone_report
from modules import drone_status
from modules import location
from modules.private.simulation import simulation_worker
from modules.private.utilities import queue_proxy_wrapper
from modules.private.utilities import worker_controller
from modules.private.utilities import worker_manager


QUEUE_MAX_SIZE = 1

# Increase the step size if your computer is lagging
# Larger step size is smaller FPS
TIME_STEP_SIZE = 0.01  # seconds
ACCEPTANCE_RADIUS = 0.1  # metres
PIXELS_PER_METRE = 60
IMAGE_RESOLUTION_X = 1200
IMAGE_RESOLUTION_Y = 900
MAP_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/world")
LANDING_PAD_IMAGES_PATH = pathlib.Path("modules/private/simulation/mapping/assets")


# Extra variables required for management
# pylint: disable-next=too-many-locals
def main() -> int:
    """
    main.
    """
    # Setup
    controller = worker_controller.WorkerController()

    mp_manager = mp.Manager()

    decision_to_simulation_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )
    simulation_to_detect_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
        QUEUE_MAX_SIZE,
    )

    worker_status_queue = queue_proxy_wrapper.QueueProxyWrapper(
        mp_manager,
    )

    drone_initial_position = location.Location(0.0, 0.0)
    landing_pad_locations = [
        location.Location(0.0, 0.0),
        location.Location(-40.0, 0.5),
    ]

    simulation_manager = worker_manager.WorkerManager()
    simulation_manager.create_workers(
        1,
        simulation_worker.simulation_worker,
        (
            TIME_STEP_SIZE,
            drone_initial_position,
            location.Location(-51.0, -38.5),
            location.Location(51.0, 38.5),
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

    simulation_manager.start_workers()

    # 0: Top right corner
    # 1: Bottom right corner
    # 2: Centre
    # 3: Bottom left corner
    # 4: Top left corner
    # 5: Centre
    # 6: Left
    # 7: Centre
    waypoint_index = 0
    waypoints = [
        commands.Command.create_set_relative_destination_command(50.0, 37.5),
        commands.Command.create_set_relative_destination_command(0.0, -75.0),
        commands.Command.create_set_relative_destination_command(-50.0, 37.5),
        commands.Command.create_set_relative_destination_command(-50.0, -37.5),
        commands.Command.create_set_relative_destination_command(0.0, 75.0),
        commands.Command.create_set_relative_destination_command(50.0, -37.5),
        commands.Command.create_set_relative_destination_command(-50.0, 0.0),
        commands.Command.create_set_relative_destination_command(50.0, 0.0),
        commands.Command.create_land_command(),
    ]

    report = drone_report.DroneReport(
        drone_status.DroneStatus.HALTED,
        drone_initial_position,
        drone_initial_position,
    )
    counter = 0
    while counter < 11000:
        output_data: "tuple[drone_report.DroneReport, list, np.ndarray]" = (
            simulation_to_detect_queue.queue.get()
        )
        report, _, camera_image = output_data

        # Pylint has issues with OpenCV
        # pylint: disable=no-member
        cv2.namedWindow("Map", cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow("Map", camera_image.shape[1] // 2, camera_image.shape[0] // 2)
        cv2.imshow("Map", camera_image)
        cv2.waitKey(1)
        # pylint: enable=no-member

        command = commands.Command.create_null_command()
        if report.status == drone_status.DroneStatus.HALTED:
            print(counter)
            print(waypoint_index)
            print("Halt: " + str(report.position))
            command = waypoints[waypoint_index]
            waypoint_index += 1
        elif report.status == drone_status.DroneStatus.LANDED:
            break

        decision_to_simulation_queue.queue.put(command)

        counter += 1

    # Teardown
    controller.request_exit()

    decision_to_simulation_queue.fill_and_drain_queue()
    simulation_to_detect_queue.fill_and_drain_queue()

    worker_status_queue.fill_and_drain_queue()

    simulation_manager.join_workers()

    # Test
    print("At: " + str(report.position))
    print("Steps: " + str(counter))

    if report.status != drone_status.DroneStatus.LANDED:
        return -2

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    status = main()
    if status < 0:
        print("ERROR: Status code: " + str(status))

    print("Done!")
