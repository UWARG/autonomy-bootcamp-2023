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

# (nothing here anymore)

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

        # Ultralytics has documentation and examples

        # Use the model's predict() method to run inference
        # Parameters of interest:
        # * source
        # * conf
        # * device
        # * verbose
        results = self.__model.predict(
            source=image,
            conf=0.25,  # keep default; lower only if needed
            iou=0.5,
            device=self.__DEVICE,  # use class device (GPU if available else CPU)
            verbose=False,
        )

        # First (and only) Result object
        prediction = results[0]

        # Annotated image (NumPy, BGR) with confidences drawn
        image_annotated = prediction.plot(conf=True, show=False)

        # If no detections, return early
        if (
            prediction.boxes is None
            or prediction.boxes.xyxy is None
            or prediction.boxes.xyxy.numel() == 0
        ):
            return [], image_annotated

        # Convert YOLO tensor -> NumPy
        xyxy = prediction.boxes.xyxy.detach().cpu().numpy()  # shape [N, 4]

        # Build BoundingBox objects EXACTLY like tests do
        bounding_boxes: list[bounding_box.BoundingBox] = []
        for x1, y1, x2, y2 in xyxy:
            ok, bb = bounding_box.BoundingBox.create(
                np.array([float(x1), float(y1), float(x2), float(y2)], dtype=float)
            )
            if ok and bb is not None:
                bounding_boxes.append(bb)

        # Make ordering deterministic to match test expectations
        bounding_boxes.sort(key=lambda b: b.x1, reverse=True)

        return bounding_boxes, image_annotated

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
