import cv2


def should_rotate_by_resolution(video_path):
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    cap.release()
    
    print(f"Detected resolution: {int(width)}x{int(height)}")
    
    # If height > width, it's portrait — no rotation needed
    return height < width