"""
Event detection logic for field hockey using YOLOv8 detection results.
Detects goals, cards, and corners from frame-by-frame object detections.
"""
from typing import List, Dict, Any

class EventDetector:
    def __init__(self):
        pass

    def detect_events(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Improved event detection logic:
        - Goal: Detects if the ball crosses the goal line (assumes 'ball' and 'goal_post' classes, uses x/y position)
        - Card: Detects card gestures (as before)
        - Corner: Detects if the ball is near the corner area (assumes field size, uses ball position)
        """
        events = []
        last_ball_pos = None
        last_goal_event = {'left': None, 'right': None}
        last_corner_event = None
        last_penalty_event = None
        last_substitution_event = None
        goal_line_x = 0.04  # Tighter goal line (4% of field width)
        field_width = 1.0
        field_height = 1.0
        corner_area = 0.08  # 8% of field width/height for corner detection
        penalty_area_x = 0.18  # 18% of field width for penalty circle (23m line)
        goal_debounce_frames = 20  # Require at least 20 frames between goal events
        corner_debounce_frames = 12
        penalty_debounce_frames = 20
        substitution_debounce_frames = 20
        ball_traj = []

        for idx, det in enumerate(detections):
            frame = det.get('frame')
            objects = det.get('objects', [])
            ball = None
            goals = []
            for obj in objects:
                if obj['class'] == 'ball' and obj['conf'] > 0.65:
                    ball = obj
                if obj['class'] == 'goal_post' and obj['conf'] > 0.65:
                    goals.append(obj)
                if obj['class'] == 'card' and obj['conf'] > 0.8:
                    # Debounce card events: only add if not same as last frame
                    if not events or events[-1]['type'] != 'card' or events[-1]['frame'] != frame-1:
                        events.append({'type': 'card', 'frame': frame, 'details': obj})
                if obj['class'] == 'penalty' and obj['conf'] > 0.7:
                    if last_penalty_event is None or (frame - last_penalty_event > penalty_debounce_frames):
                        events.append({'type': 'penalty', 'frame': frame, 'details': obj})
                        last_penalty_event = frame
                if obj['class'] == 'substitution' and obj['conf'] > 0.7:
                    if last_substitution_event is None or (frame - last_substitution_event > substitution_debounce_frames):
                        events.append({'type': 'substitution', 'frame': frame, 'details': obj})
                        last_substitution_event = frame
            # Ball trajectory tracking
            if ball and 'bbox' in ball:
                x_center = (ball['bbox'][0] + ball['bbox'][2]) / 2.0
                y_center = (ball['bbox'][1] + ball['bbox'][3]) / 2.0
                ball_traj.append({'frame': frame, 'x': x_center, 'y': y_center})
                # Goal detection: ball crosses left or right goal line, debounce
                if x_center < field_width * goal_line_x:
                    if last_goal_event['left'] is None or (frame - last_goal_event['left'] > goal_debounce_frames):
                        recent = [b for b in ball_traj[-7:-1] if b['x'] < field_width * goal_line_x]
                        if not recent:
                            events.append({'type': 'goal', 'frame': frame, 'side': 'left', 'details': ball})
                            last_goal_event['left'] = frame
                elif x_center > field_width * (1 - goal_line_x):
                    if last_goal_event['right'] is None or (frame - last_goal_event['right'] > goal_debounce_frames):
                        recent = [b for b in ball_traj[-7:-1] if b['x'] > field_width * (1 - goal_line_x)]
                        if not recent:
                            events.append({'type': 'goal', 'frame': frame, 'side': 'right', 'details': ball})
                            last_goal_event['right'] = frame
                # Corner detection: ball in corner area, debounce
                in_corner = (
                    (x_center < field_width * corner_area and y_center < field_height * corner_area) or
                    (x_center > field_width * (1 - corner_area) and y_center < field_height * corner_area) or
                    (x_center < field_width * corner_area and y_center > field_height * (1 - corner_area)) or
                    (x_center > field_width * (1 - corner_area) and y_center > field_height * (1 - corner_area))
                )
                if in_corner:
                    if last_corner_event is None or (frame - last_corner_event > corner_debounce_frames):
                        recent = [b for b in ball_traj[-5:-1] if (
                            (b['x'] < field_width * corner_area and b['y'] < field_height * corner_area) or
                            (b['x'] > field_width * (1 - corner_area) and b['y'] < field_height * corner_area) or
                            (b['x'] < field_width * corner_area and b['y'] > field_height * (1 - corner_area)) or
                            (b['x'] > field_width * (1 - corner_area) and b['y'] > field_height * (1 - corner_area))
                        )]
                        if not recent:
                            events.append({'type': 'corner', 'frame': frame, 'details': ball})
                            last_corner_event = frame
                # Penalty detection: ball enters penalty area (23m circle)
                in_penalty = (x_center < field_width * penalty_area_x) or (x_center > field_width * (1 - penalty_area_x))
                if in_penalty:
                    if last_penalty_event is None or (frame - last_penalty_event > penalty_debounce_frames):
                        recent = [b for b in ball_traj[-5:-1] if (b['x'] < field_width * penalty_area_x or b['x'] > field_width * (1 - penalty_area_x))]
                        if not recent:
                            events.append({'type': 'penalty_area_entry', 'frame': frame, 'details': ball})
                            last_penalty_event = frame
            last_ball_pos = ball
        return events
