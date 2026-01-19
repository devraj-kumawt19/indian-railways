try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
from typing import List, Tuple

class FrameProcessor:
    """Processes video frames for train detection."""

    def __init__(self, resize_width: int = 640, resize_height: int = 480):
        self.resize_width = resize_width
        self.resize_height = resize_height

    def extract_frames(self, video_path: str, interval: int = 30) -> List:
        """Extract frames from video at specified intervals."""
        if not OPENCV_AVAILABLE:
            return []
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % interval == 0:
                processed_frame = self.preprocess_frame(frame)
                frames.append(processed_frame)

            frame_count += 1

        cap.release()
        return frames

    def preprocess_frame(self, frame):
        """Preprocess frame: resize, normalize, etc."""
        if not OPENCV_AVAILABLE or frame is None:
            return None
        # Resize frame
        resized = cv2.resize(frame, (self.resize_width, self.resize_height))

        # Convert to RGB if needed
        if len(resized.shape) == 3 and resized.shape[2] == 3:
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        return resized

    def detect_motion(self, prev_frame, curr_frame, threshold: int = 25) -> Tuple[bool, None]:
        """Detect motion between frames."""
        if not OPENCV_AVAILABLE or prev_frame is None or curr_frame is None:
            return False, None
        # Convert to grayscale
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_RGB2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)

        # Calculate difference
        frame_diff = cv2.absdiff(prev_gray, curr_gray)

        # Apply threshold
        _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if motion detected
        motion_detected = len(contours) > 0

        return motion_detected, thresh