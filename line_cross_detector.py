import cv2

def segments_intersect(p1, p2, q1, q2):
    """Check if line segments p1→p2 and q1→q2 intersect."""
    def ccw(a, b, c):
        return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
    return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

class LineCrossDetector:
    def __init__(self, line_start, line_end):
        self.line_start = line_start  # (x, y)
        self.line_end = line_end      # (x, y)
        self.previous_positions = {}  # {id: (cx, cy)}
        self.crossed_ids = set()

    def has_crossed(self, obj_id, current_point):
        if obj_id in self.crossed_ids:
            return False

        if obj_id in self.previous_positions:
            prev_point = self.previous_positions[obj_id]

            # Check if the movement line intersects the detection line
            if segments_intersect(prev_point, current_point, self.line_start, self.line_end):
                self.crossed_ids.add(obj_id)
                self.previous_positions[obj_id] = current_point
                return True

        # Update position
        self.previous_positions[obj_id] = current_point
        return False

    def reset(self):
        self.previous_positions.clear()
        self.crossed_ids.clear()