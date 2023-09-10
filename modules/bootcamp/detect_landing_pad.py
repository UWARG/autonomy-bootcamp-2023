"""
BOOTCAMPERS TO COMPLETE.

Detects landing pads.
"""
import pathlib

import numpy as np
import torch
import ultralytics

from .. import bounding_box


# This is just an interface
# pylint: disable=too-few-public-methods
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
    def create(cls, model_directory: pathlib.Path):
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

    def __init__(self, class_private_create_key, model: ultralytics.YOLO):
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

        # Ultralytics has documentation and examples

        # Use the model's predict() method to run inference
        # Parameters of interest:
        # * source
        # * conf
        # * device
        # * verbose
        predictions = ...

        # Get the Result object
        prediction = ...

        # Plot the annotated image from the Result object
        # Include the confidence value
        image_annotated = ...

        # Get the xyxy boxes list from the Boxes object in the Result object
        boxes_xyxy = ...

        # Detach the xyxy boxes to make a copy,
        # move the copy into CPU space,
        # and convert to a numpy array
        boxes_cpu = ...

        # Loop over the boxes list and create a list of bounding boxes
        bounding_boxes = []
        # Hint: .shape gets the dimensions of the numpy array
        # for i in range(0, ...):
            # Create BoundingBox object and append to list
            # result, box = ...

        # Remove this when done
        raise NotImplementedError

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
