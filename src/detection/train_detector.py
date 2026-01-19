try:
    import cv2
except ImportError:
    cv2 = None

class TrainDetector:
    """Detects trains in video frames using YOLO."""

    def __init__(self, model_path: str = "models/yolov8n.pt"):
        # Try to import YOLO when needed
        self.YOLO_AVAILABLE = False
        self.YOLO = None
        self.model = None

        try:
            from ultralytics import YOLO
            import numpy as np
            self.YOLO_AVAILABLE = True
            self.YOLO = YOLO
            try:
                self.model = YOLO(model_path)
            except Exception as model_error:
                # Model loading failed, continue with inference disabled
                print(f"Warning: Could not load YOLO model from {model_path}: {model_error}")
                self.YOLO_AVAILABLE = False
        except ImportError as import_error:
            print(f"Warning: YOLO not available: {import_error}")
            self.YOLO_AVAILABLE = False
        self.train_classes = ['train', 'locomotive', 'railway_car']  # Adjust based on model

    def detect_train(self, frame):
        """Check if a train is present in the frame."""
        if not self.YOLO_AVAILABLE or self.model is None or frame is None:
            return False

        try:
            results = self.model(frame, conf=0.5)
            detections = results[0].boxes

            for detection in detections:
                class_id = int(detection.cls)
                class_name = self.model.names[class_id]
                if class_name.lower() in [cls.lower() for cls in self.train_classes]:
                    return True
        except Exception as e:
            # Log error but don't crash - fail safely
            print(f"Error detecting train: {e}")
            return False

        return False

    def get_train_bbox(self, frame):
        """Get bounding boxes of detected trains."""
        if not self.YOLO_AVAILABLE or self.model is None or frame is None:
            return []

        try:
            results = self.model(frame, conf=0.5)
            detections = results[0].boxes

            bboxes = []
            for detection in detections:
                class_id = int(detection.cls)
                class_name = self.model.names[class_id]
                if class_name.lower() in [cls.lower() for cls in self.train_classes]:
                    x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy()
                    bboxes.append((int(x1), int(y1), int(x2), int(y2)))

            return bboxes
        except Exception as e:
            # Log error but fail gracefully
            print(f"Error getting train bboxes: {e}")
            return []