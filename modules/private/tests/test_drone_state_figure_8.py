"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Test drone state simulation with a figure 8.
"""

from modules import commands
from modules import drone_status
from modules import location
from modules.private.simulation.drone import drone_state


TIME_STEP_SIZE = 0.01  # seconds
ACCEPTANCE_RADIUS = 0.1  # metres


def main() -> int:
    """
    main.
    """
    initial_position = location.Location(0.0, 0.0)
    boundary_bottom_left = location.Location(-11.0, -11.0)
    boundary_top_right = location.Location(11.0, 11.0)
    result, drone = drone_state.DroneState.create(
        TIME_STEP_SIZE,
        initial_position,
        boundary_bottom_left,
        boundary_top_right,
        ACCEPTANCE_RADIUS,
    )
    if not result:
        return -1

    # Get Pylance to stop complaining
    assert drone is not None

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
        commands.Command.create_set_relative_destination_command(3.0, 4.0),
        commands.Command.create_set_relative_destination_command(0.0, -8.0),
        commands.Command.create_set_relative_destination_command(-3.0, 4.0),
        commands.Command.create_set_relative_destination_command(-3.0, -4.0),
        commands.Command.create_set_relative_destination_command(0.0, 8.0),
        commands.Command.create_set_relative_destination_command(3.0, -4.0),
        commands.Command.create_set_relative_destination_command(-3.0, 0.0),
        commands.Command.create_set_relative_destination_command(3.0, 0.0),
        commands.Command.create_land_command(),
    ]

    report, step = drone.run(commands.Command.create_null_command())
    while report.status != drone_status.DroneStatus.LANDED and step < 1000:
        command = commands.Command.create_null_command()
        if report.status == drone_status.DroneStatus.HALTED:
            print(step)
            print(waypoint_index)
            print(f"Halt: {report.position}")
            command = waypoints[waypoint_index]
            waypoint_index += 1

        report, step = drone.run(command)

    print(f"At: {report.position}")
    print(f"Steps: {step}")

    if report.status != drone_status.DroneStatus.LANDED:
        return -2

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
