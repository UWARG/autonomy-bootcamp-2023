"""
BOOTCAMPERS DO NOT MODIFY THIS FILE.

Displays the map and drone information.
"""
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
    __LANDING_IMAGE_NAME = "landing_screenshot.png"

    @classmethod
    def create(cls, display_scale: float, enable_logging: bool) -> "tuple[bool, Display | None]":
        """
        display_scale: Scale of the displayed image from 0 to 1.
        """
        if display_scale <= 0.0:
            return False, None

        return True, Display(cls.__create_key, display_scale, enable_logging)

    def __init__(self, class_private_create_key, display_scale: float, enable_logging: bool):
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Display.__create_key, "Use create() method"

        self.__display_scale = display_scale
        self.__has_saved_landing_image = not enable_logging

    @staticmethod
    def __display(image: np.ndarray, display_scale: float):
        """
        Displays the provided image.
        """
        # Pylint has issues with OpenCV
        # pylint: disable=no-member
        cv2.namedWindow("Display", cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(
            "Display",
            int(image.shape[1] * display_scale),
            int(image.shape[0] * display_scale),
        )
        cv2.imshow("Display", image)
        cv2.waitKey(1)
        # pylint: enable=no-member

    @staticmethod
    # Extra variables required for display
    # pylint: disable-next=too-many-locals
    def __generate_information_pane(resolution_x: int,
                                    resolution_y: int,
                                    report: drone_report.DroneReport) -> np.ndarray:
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
        position_x_text = "x: " + str(report.position.location_x)
        position_y_text = "y: " + str(report.position.location_y)
        position_colour = (255, 255, 255)  # White

        destination_text = "Destination: None"
        destination_x_text = ""
        destination_y_text = ""
        destination_colour = (255, 255, 0)  # Cyan
        if report.status == drone_status.DroneStatus.MOVING:
            destination_text = "Destination:"
            destination_x_text = "x: " + str(report.destination.location_x)
            destination_y_text = "y: " + str(report.destination.location_y)

        text_x = 45
        text_line_y = 45
        text_line_counter = 2
        text_size = 1.0

        image = np.zeros((resolution_y, resolution_x, 3))

        # Pylint has issues with OpenCV
        # pylint: disable=no-member
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
        # pylint: enable=no-member

        return image

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
        )

        display_image = np.concatenate((map_image, pane_image), axis=1)

        # Save landing image
        if not self.__has_saved_landing_image and report.status == drone_status.DroneStatus.LANDED:
            prefix_text = str(int(time.time()))
            # Pylint has issues with OpenCV
            # pylint: disable-next=no-member
            cv2.imwrite(prefix_text + "_" + self.__LANDING_IMAGE_NAME, display_image)

            self.__has_saved_landing_image = True

        self.__display(display_image, self.__display_scale)

        return True
