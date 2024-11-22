"""
BOOTCAMPERS TO COMPLETE.

Detects landing pads.
"""

import pathlib

import numpy as np
import torch
import ultralytics

from .. import bounding_box


# ============
# ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# ============
# Bootcampers remove the following lines:
# Allow linters and formatters to pass for bootcamp maintainers
# No enable
# pylint: disable=unused-argument,unused-private-member,unused-variable
# ============
# ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# ============


class DetectLandingPad:
    """
    Contains the YOLOv8 model for prediction.
    """

    __create_key = object()

    # ============
    # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
    # ============

    # Chooses the GPU if it exists, otherwise runs on the CPU
    # If you have a CUDA capable GPU but want to force it to
    # run on the CPU instead, replace the right side with "cpu"
    __DEVICE = 0 if torch.cuda.is_available() else "cpu"

    # ============
    # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
    # ============

    __MODEL_NAME = "best-2n.pt"

    @classmethod
    def create(cls, model_directory: pathlib.Path) -> "tuple[bool, DetectLandingPad | None]":
        """
        model_directory: Directory to models.
        """
        if not model_directory.is_dir():
            return False, None

        model_path = pathlib.PurePosixPath(
            model_directory,
            cls.__MODEL_NAME,
        )

        try:
            model = ultralytics.YOLO(str(model_path))
        # Library can throw any exception
        # pylint: disable-next=broad-exception-caught
        except Exception:
            return False, None

        return True, DetectLandingPad(cls.__create_key, model)

    def __init__(self, class_private_create_key: object, model: ultralytics.YOLO) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is DetectLandingPad.__create_key, "Use create() method"

        self.__model = model

    def run(self, image: np.ndarray) -> "tuple[list[bounding_box.BoundingBox], np.ndarray]":
        """
        Converts an image into a list of bounding boxes.

        image: The image to run on.

        Return: A tuple of (list of bounding boxes, annotated image) .
            The list of bounding boxes can be empty.
        """
        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        outcome = self.__model.predict(source = image, conf = 0.7, device = self.__DEVICE, verbose = 0)
        prediction = outcome[0]

        img = prediction.plot(conf = 1)
        boxes = prediction.boxes.xyxy
        boxes_cpu = boxes.detach().cpu().numpy()

        bounding_boxes = []
        for i in range(0, boxes_cpu.shape[0]):
            result, box = bounding_box.BoundingBox.create(boxes_cpu[i])
            if not result:
                return [], img
            bounding_boxes.append(box)
        return bounding_boxes, img
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
