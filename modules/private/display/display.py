"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Displays the map and drone information.
"""

import pathlib
import time

import cv2
import numpy as np

from ... import drone_report
from ... import drone_status


class Display:
    """
    Draws the display.
    """

    __create_key = object()

    __PANE_RESOLUTION_X = 400
    __IMAGE_SAVE_DIRECTORY = pathlib.Path("log")
    __LANDING_IMAGE_NAME = "landing_screenshot.png"

    @classmethod
    def create(cls, display_scale: float, seed: int) -> "tuple[bool, Display | None]":
        """
        display_scale: Scale of the displayed image from 0 to 1.
        seed: Seed of the simulation generator.
        """
        if display_scale <= 0.0:
            return False, None

        cls.__IMAGE_SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)

        return True, Display(cls.__create_key, display_scale, seed)

    def __init__(self, class_private_create_key: object, display_scale: float, seed: int) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Display.__create_key, "Use create() method"

        self.__display_scale = display_scale
        self.__has_saved_landing_image = False

        self.__seed = seed

    @staticmethod
    def __display(image: np.ndarray, display_scale: float) -> None:
        """
        Displays the provided image.
        """
        cv2.namedWindow("Display", cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(
            "Display",
            int(image.shape[1] * display_scale),
            int(image.shape[0] * display_scale),
        )
        cv2.imshow("Display", image)
        cv2.waitKey(1)

    @staticmethod
    def __generate_information_pane(
        resolution_x: int, resolution_y: int, report: drone_report.DroneReport, seed: int
    ) -> np.ndarray:
        """
        Draws the information pane from the drone report.
        """
        # Colour is in BGR

        status_text = "Status: ERROR"
        status_colour = (0, 0, 255)  # Red
        if report.status == drone_status.DroneStatus.HALTED:
            status_text = "Status: HALTED"
            status_colour = (0, 255, 255)  # Yellow
        elif report.status == drone_status.DroneStatus.MOVING:
            status_text = "Status: MOVING"
            status_colour = (255, 0, 255)  # Magenta
        elif report.status == drone_status.DroneStatus.LANDED:
            status_text = "Status: LANDED"
            status_colour = (0, 255, 0)  # Green

        position_text = "Position:"
        position_x_text = f"x: {report.position.location_x:7.3f}"
        position_y_text = f"y: {report.position.location_y:7.3f}"
        position_colour = (255, 255, 255)  # White

        destination_text = "Destination: None"
        destination_x_text = ""
        destination_y_text = ""
        destination_colour = (255, 255, 0)  # Cyan
        if report.status == drone_status.DroneStatus.MOVING:
            destination_text = "Destination:"
            destination_x_text = f"x: {report.destination.location_x:7.3f}"
            destination_y_text = f"y: {report.destination.location_y:7.3f}"

        seed_text = "Seed:"
        seed_value_text = str(seed)
        seed_colour = (255, 255, 255)  # White

        text_x = 45
        text_line_y = 45
        text_line_counter = 2
        text_size = 1.0

        image = np.zeros((resolution_y, resolution_x, 3), dtype=np.uint8)

        _ = cv2.putText(
            image,
            status_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            status_colour,
            2,
        )
        text_line_counter += 1

        _ = cv2.putText(
            image,
            position_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            position_colour,
            2,
        )
        text_line_counter += 1

        _ = cv2.putText(
            image,
            position_x_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            position_colour,
            2,
        )
        text_line_counter += 1

        _ = cv2.putText(
            image,
            position_y_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            position_colour,
            2,
        )
        text_line_counter += 1
        text_line_counter += 1

        _ = cv2.putText(
            image,
            destination_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            destination_colour,
            2,
        )
        text_line_counter += 1

        _ = cv2.putText(
            image,
            destination_x_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            destination_colour,
            2,
        )
        text_line_counter += 1

        _ = cv2.putText(
            image,
            destination_y_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            destination_colour,
            2,
        )
        text_line_counter += 1
        text_line_counter += 1

        _ = cv2.putText(
            image,
            seed_text,
            (text_x, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            seed_colour,
            2,
        )
        text_line_counter += 1

        _ = cv2.putText(
            image,
            seed_value_text,
            (0, text_line_y * text_line_counter),
            cv2.FONT_HERSHEY_SIMPLEX,
            text_size,
            seed_colour,
            2,
        )
        text_line_counter += 1

        return image

    @staticmethod
    def __draw_map_ui_elements(map_image: np.ndarray) -> None:
        """
        Draws map UI elements on the provided image.

        map_image: Image to be mutated.
        """
        centre_circle_radius = 30
        centre_circle_colour = (0, 255, 0)  # Green, BGR
        centre_circle_line_thickness = 2

        cv2.circle(
            map_image,
            (map_image.shape[1] // 2, map_image.shape[0] // 2),
            centre_circle_radius,
            centre_circle_colour,
            centre_circle_line_thickness,
        )

    def run(self, report: drone_report.DroneReport, map_image: np.ndarray) -> bool:
        """
        Display.
        """
        if len(map_image.shape) != 3:
            return False

        if map_image.shape[2] != 3:
            return False

        pane_image = self.__generate_information_pane(
            self.__PANE_RESOLUTION_X,
            map_image.shape[0],
            report,
            self.__seed,
        )

        self.__draw_map_ui_elements(map_image)

        display_image = np.concatenate((map_image, pane_image), axis=1)

        # Save landing image
        if not self.__has_saved_landing_image and report.status == drone_status.DroneStatus.LANDED:
            image_name = f"{int(time.time())}_{self.__LANDING_IMAGE_NAME}"
            image_path = pathlib.PurePosixPath(self.__IMAGE_SAVE_DIRECTORY, image_name)
            cv2.imwrite(str(image_path), display_image)

            self.__has_saved_landing_image = True

        self.__display(display_image, self.__display_scale)

        return True
