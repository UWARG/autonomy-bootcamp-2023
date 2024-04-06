"""
BOOTCAMPERS TO COMPLETE.

Detects landing pads.
"""
import pathlib

import numpy as np
import torch
import ultralytics

from .. import bounding_box


class DetectLandingPad:
    """
    Contains the YOLOv8 model for prediction.
    """
    __create_key = object()
    __DEVICE = 0 if torch.cuda.is_available() else "cpu"


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

        predictions = self.__model.predict(source=image, conf=0.7, device=self.__DEVICE, verbose=False)

        prediction = predictions[0]

        image_annotated = prediction.plot()

        boxes_xyxy = prediction.boxes.xyxy

        boxes_cpu = boxes_xyxy.detach().cpu().numpy()

        bounding_boxes = []
        for i in range(boxes_cpu.shape[0]):
            bounds = boxes_cpu[i]
            success, box = bounding_box.BoundingBox.create(bounds)
            if not success:
                return [], image_annotated
            bounding_boxes.append(box)

        return bounding_boxes, image_annotated
