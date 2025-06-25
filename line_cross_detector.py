import cv2
import numpy as np

class LineCrossDetector:
    def __init__(self, line_start, line_end, buffer=15):
        self.line_start = line_start
        self.line_end = line_end
        self.buffer = buffer  # pixels to extend the detection zone
        self.previous_positions = {}  # object_id: (x, y)
        self.crossed_ids = set()
        self._create_detection_zone()

    def _create_detection_zone(self):
        """Creates a thick rectangle polygon around the line."""
        x1, y1 = self.line_start
        x2, y2 = self.line_end

        # Vector perpendicular to the line
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy)
        if length == 0:
            self.detection_zone = None
            return

        # Normalize perpendicular vector
        nx, ny = -dy / length, dx / length

        # Create a rectangle around the line
        offset_x, offset_y = nx * self.buffer, ny * self.buffer

        pt1 = (int(x1 + offset_x), int(y1 + offset_y))
        pt2 = (int(x2 + offset_x), int(y2 + offset_y))
        pt3 = (int(x2 - offset_x), int(y2 - offset_y))
        pt4 = (int(x1 - offset_x), int(y1 - offset_y))

        self.detection_zone = np.array([pt1, pt2, pt3, pt4], dtype=np.int32)
    def draw_line(self, img, color=(0, 0, 255), THICKNESS=1):
        cv2.line(img, self.line_start, self.line_end, color, thickness=THICKNESS)

    def draw_detection_zone(self, img):
        """Draws the buffer zone on the image (for debugging)."""
        self._create_detection_zone()
        if self.detection_zone is not None:
            cv2.polylines(img, [self.detection_zone], isClosed=True, color=(255, 255, 0), thickness=2)

    def has_crossed(self, obj_id, current_point):
        if self.detection_zone is None:
            return False

        if obj_id in self.crossed_ids:
            return False

        if obj_id in self.previous_positions:
            prev_point = self.previous_positions[obj_id]

            # Check if previous and current point are on opposite sides of the zone
            inside_prev = cv2.pointPolygonTest(self.detection_zone, prev_point, measureDist=False)
            inside_curr = cv2.pointPolygonTest(self.detection_zone, current_point, measureDist=False)

            if inside_prev < 0 and inside_curr > 0:
                # Crossed into the zone
                self.crossed_ids.add(obj_id)
                self.previous_positions[obj_id] = current_point
                return True
            elif inside_prev > 0 and inside_curr < 0:
                # Crossed out of the zone
                self.crossed_ids.add(obj_id)
                self.previous_positions[obj_id] = current_point
                return True

        # Update previous position
        self.previous_positions[obj_id] = current_point
        return False

    def reset(self):
        self.previous_positions.clear()
        self.crossed_ids.clear()