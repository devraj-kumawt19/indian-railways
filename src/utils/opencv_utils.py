try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

from typing import List, Tuple, Optional
from src.utils.logging_config import get_logger

logger = get_logger("opencv_utils")


class FrameProcessor:
    """Processes video frames for train detection.

    Improvements:
    - explicit typing
    - robust grayscale conversion (handles RGB/BGR)
    - compatibility with different OpenCV `findContours` signatures
    - logging for easier debugging
    """

    def __init__(self, resize_width: int = 640, resize_height: int = 480):
        self.resize_width = int(resize_width)
        self.resize_height = int(resize_height)

    def extract_frames(self, video_path: str, interval: int = 30) -> List[np.ndarray]:
        """Extract frames from video at specified intervals.

        Returns a list of preprocessed frames (as numpy arrays). If OpenCV
        isn't available or the video cannot be opened, an empty list is
        returned.
        """
        if not OPENCV_AVAILABLE:
            logger.warning("OpenCV not available; extract_frames will return empty list")
            return []

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.warning("Failed to open video: %s", video_path)
            return []

        frames: List[np.ndarray] = []
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % interval == 0:
                processed_frame = self.preprocess_frame(frame)
                if processed_frame is not None:
                    frames.append(processed_frame)

            frame_count += 1

        cap.release()
        logger.debug("Extracted %d frames from %s", len(frames), video_path)
        return frames

    def preprocess_frame(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """Preprocess frame: resize and ensure a consistent color layout.

        This method keeps frames as BGR (OpenCV default) to remain compatible
        with OpenCV algorithms. If you need RGB for visualization, convert
        at the display layer instead.
        """
        if not OPENCV_AVAILABLE or frame is None:
            return None

        try:
            resized = cv2.resize(frame, (self.resize_width, self.resize_height))
        except Exception as e:
            logger.exception("Failed to resize frame: %s", e)
            return None

        # Keep in BGR for consistent processing
        return resized

    def _to_grayscale(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """Convert a color frame to grayscale robustly handling RGB/BGR."""
        if frame is None:
            return None

        try:
            if len(frame.shape) == 2:
                return frame
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                # Try common conversions; some pipelines provide RGB, others BGR
                try:
                    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                except cv2.error:
                    return cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # Fallback
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            logger.exception("Grayscale conversion failed: %s", e)
            return None

    def detect_motion(self, prev_frame: np.ndarray, curr_frame: np.ndarray, threshold: int = 25) -> Tuple[bool, Optional[np.ndarray]]:
        """Detect motion between frames.

        Returns a tuple of (motion_detected: bool, mask: Optional[np.ndarray]).
        The mask is a binary image of regions that changed.
        """
        if not OPENCV_AVAILABLE:
            logger.debug("OpenCV not available; detect_motion returns no motion")
            return False, None
        if prev_frame is None or curr_frame is None:
            return False, None

        prev_gray = self._to_grayscale(prev_frame)
        curr_gray = self._to_grayscale(curr_frame)
        if prev_gray is None or curr_gray is None:
            return False, None

        # Calculate absolute difference and threshold
        frame_diff = cv2.absdiff(prev_gray, curr_gray)
        _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

        # Optional: reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        # Find contours with compatibility for OpenCV versions
        try:
            contours_info = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours_info) == 3:
                _, contours, _ = contours_info
            else:
                contours, _ = contours_info
        except Exception as e:
            logger.exception("findContours failed: %s", e)
            return False, thresh

        motion_detected = any(cv2.contourArea(c) > 10 for c in contours)

        return motion_detected, thresh