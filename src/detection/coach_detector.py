try:
    import cv2
except ImportError:
    cv2 = None

class CoachDetector:
    """Advanced train coach detection and identification system."""

    def __init__(self, model_path="models/yolov8n.pt"):
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
            except Exception as e:
                print(f"Warning: Could not load YOLO model: {e}")
                pass
        except ImportError as e:
            print(f"Warning: YOLO not available: {e}")
            self.YOLO_AVAILABLE = False

        # Enhanced coach classes for better detection
        self.coach_classes = [
            'coach', 'railway_car', 'wagon', 'train_car', 'passenger_car',
            'locomotive', 'engine', 'caboose', 'baggage_car', 'dining_car'
        ]

        # Indian Railways coach type mapping
        self.coach_types = {
            'A': 'AC First Class',
            'B': 'AC 2-Tier',
            'C': 'AC 3-Tier',
            'D': 'AC Chair Car',
            'E': 'Executive Chair Car',
            'G': 'Garib Rath',
            'H': 'AC 3-Tier Economy',
            'J': 'AC 2-Tier Garib Rath',
            'K': 'AC 3-Tier Garib Rath',
            'L': 'AC Chair Car Garib Rath',
            'M': 'AC Chair Car Executive',
            'S': 'Sleeper Class',
            'U': 'AC 3-Tier Economy',
            'V': 'Vistadome AC Chair Car',
            'W': 'AC 2-Tier Economy'
        }

    def detect_coaches(self, frame):
        """Detect coaches and return their detailed information."""
        if not self.YOLO_AVAILABLE or self.model is None or frame is None:
            return []

        try:
            results = self.model(frame, conf=0.3)  # Lower confidence for better detection
            detections = results[0].boxes

            coaches = []
            for detection in detections:
                class_id = int(detection.cls)
                class_name = self.model.names[class_id]

                # Check if it's a coach/train related object
                if any(cls.lower() in class_name.lower() for cls in self.coach_classes):
                    x1, y1, x2, y2 = detection.xyxy[0].cpu().numpy()
                    conf = detection.conf[0].cpu().numpy()

                    # Calculate additional properties
                    width = int(x2 - x1)
                    height = int(y2 - y1)
                    area = width * height
                    aspect_ratio = width / height if height > 0 else 0

                    coach_info = {
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'confidence': float(conf),
                        'class': class_name,
                        'center_x': int((x1 + x2) / 2),
                        'center_y': int((y1 + y2) / 2),
                        'width': width,
                        'height': height,
                        'area': area,
                        'aspect_ratio': aspect_ratio,
                        'coach_type': self._classify_coach_type(width, height, aspect_ratio),
                        'position': None,  # Will be set by assign_coach_numbers
                        'number': None    # Will be set by assign_coach_numbers
                    }
                    coaches.append(coach_info)

            return coaches
        except Exception as e:
            print(f"Coach detection error: {e}")
            return []

    def _classify_coach_type(self, width, height, aspect_ratio):
        """Classify coach type based on dimensions and aspect ratio."""
        # Simple classification based on aspect ratio and size
        if aspect_ratio > 2.5:  # Long and narrow - likely locomotive
            return "Locomotive"
        elif aspect_ratio > 1.8:  # Moderately long - passenger coach
            if width > 150:  # Large coach
                return "Passenger Coach"
            else:  # Smaller coach
                return "Shorter Coach"
        elif aspect_ratio > 1.2:  # Square-ish - could be special coach
            return "Special Coach"
        else:  # Square or vertical - possibly wagon or special car
            return "Wagon/Special Car"

    def identify_engine_and_guard(self, coaches):
        """Identify engine (front) and guard (back) from coaches."""
        if not coaches:
            return None, None

        # Sort by x-coordinate (assuming train moves left to right)
        sorted_coaches = sorted(coaches, key=lambda x: x['center_x'])

        # First coach is typically the engine (front)
        engine = sorted_coaches[0]

        # Last coach is typically the guard (back)
        guard = sorted_coaches[-1]

        # Mark their positions
        engine['position'] = 'Engine'
        guard['position'] = 'Guard'

        return engine, guard

    def assign_coach_numbers(self, coaches):
        """Assign coach numbers and positions based on detection."""
        if not coaches:
            return coaches

        # Sort from front to back (left to right in image)
        sorted_coaches = sorted(coaches, key=lambda x: x['center_x'])

        # Identify engine and guard first
        engine, guard = self.identify_engine_and_guard(sorted_coaches)

        # Standard Indian Railways coach numbering (from engine to guard)
        # A typical train composition: Engine - A1, B1, S1-S6, B2, A2 - Guard
        coach_sequence = [
            ('Engine', 'ENG'),
            ('AC First Class', 'A1'),
            ('AC 2-Tier', 'B1'),
            ('Sleeper', 'S1'),
            ('Sleeper', 'S2'),
            ('Sleeper', 'S3'),
            ('Sleeper', 'S4'),
            ('Sleeper', 'S5'),
            ('Sleeper', 'S6'),
            ('AC 2-Tier', 'B2'),
            ('AC First Class', 'A2'),
            ('Guard', 'GRD')
        ]

        # Assign numbers to detected coaches
        for i, coach in enumerate(sorted_coaches):
            if i < len(coach_sequence):
                coach_type, coach_number = coach_sequence[i]
                coach['coach_type_full'] = coach_type
                coach['number'] = coach_number
                coach['position'] = f"Position {i+1}"
            else:
                coach['coach_type_full'] = "Additional Coach"
                coach['number'] = f"C{i+1}"
                coach['position'] = f"Position {i+1}"

        return sorted_coaches

    def draw_coach_detections(self, frame, coaches):
        """Draw coach detections on the frame with labels."""
        if frame is None:
            return frame

        frame_copy = frame.copy()

        for coach in coaches:
            bbox = coach['bbox']
            x1, y1, x2, y2 = bbox

            # Choose color based on coach type
            if coach.get('position') == 'Engine':
                color = (0, 255, 0)  # Green for engine
            elif coach.get('position') == 'Guard':
                color = (0, 0, 255)  # Red for guard
            else:
                color = (255, 165, 0)  # Orange for other coaches

            # Draw bounding box
            cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)

            # Draw label
            label = f"{coach.get('number', 'Unknown')}"
            conf = coach.get('confidence', 0)
            label += f" ({conf:.2f})"

            # Draw label background
            (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame_copy, (x1, y1 - label_height - baseline), (x1 + label_width, y1), color, -1)

            # Draw label text
            cv2.putText(frame_copy, label, (x1, y1 - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame_copy

    def get_coach_summary(self, coaches):
        """Get summary statistics of detected coaches."""
        if not coaches:
            return {
                'total_coaches': 0,
                'engine_detected': False,
                'guard_detected': False,
                'coach_types': {},
                'average_confidence': 0.0
            }

        total_coaches = len(coaches)
        engine_detected = any(c.get('position') == 'Engine' for c in coaches)
        guard_detected = any(c.get('position') == 'Guard' for c in coaches)

        # Count coach types
        coach_types = {}
        confidences = []

        for coach in coaches:
            coach_type = coach.get('coach_type_full', 'Unknown')
            coach_types[coach_type] = coach_types.get(coach_type, 0) + 1
            confidences.append(coach.get('confidence', 0))

        average_confidence = sum(confidences) / len(confidences) if confidences else 0

        return {
            'total_coaches': total_coaches,
            'engine_detected': engine_detected,
            'guard_detected': guard_detected,
            'coach_types': coach_types,
            'average_confidence': average_confidence,
            'detection_timestamp': None  # Could add timestamp if needed
        }