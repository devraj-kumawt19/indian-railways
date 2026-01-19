try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
from typing import Optional, Tuple

class CameraManager:
    """Manages camera input for train detection system."""

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = None

    def start_camera(self) -> bool:
        """Start the camera feed."""
        if not OPENCV_AVAILABLE:
            return False
        self.cap = cv2.VideoCapture(self.camera_index)
        return self.cap.isOpened()

    def get_frame(self):
        """Get a single frame from the camera."""
        if not OPENCV_AVAILABLE or self.cap is None or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        return frame if ret else None

    def stop_camera(self):
        """Stop the camera feed."""
        if self.cap and OPENCV_AVAILABLE:
            self.cap.release()
            self.cap = None

    def __del__(self):
        self.stop_camera()