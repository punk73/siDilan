from ultralytics import YOLO
import cv2
import cvzone
import math
import numpy as np
from sort import *
from states import saveToText, load
import tkinter as tk
from tkinter import simpledialog
import gui
from bot import send_photo, send_message
import setting
from line_cross_detector import LineCrossDetector
import model
from datetime import datetime
import time
# global var
# Line drawing variables
line_points =  load("start.json")# Store the points of the line
end =  load("end.json")# Store the points of the line
# arrow = load("arrow.json")
counter = len(line_points) + len(end)
ids = []
pelanggar = []
cross_detector_end = None
cross_detector_start = None

model.init_db()
latest_id = model.get_last_object_id()
# root = tk.Tk()
# root.withdraw()  # Hide main window
# stream_url = simpledialog.askstring("Input", "Enter CCTV link (leave blank for default):")

# URL of the HLS stream
# stream_url = 'https://cctv.purwakartakab.go.id/cctv/rel-munjul.m3u8?v=4066696'  # Example stream URL

# stream_url = 'https://s3klari.qumicon.info:8888/camFix-F2/stream.m3u8' #klari arah cikampek
# stream_url = 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8' #klari ke arah pintu toll kartim
# stream_url = 'https://s3klari.qumicon.info:8888/camFix-F1/stream.m3u8' #klari arah karawang ./test_video/test.MOV

# I want to use gui on test.py to use as stream_url, how do i do that ?

# stream_url = input("input link cctv: (enter untuk menggunakan link default)")  # Example stream URL



        
def main():
    global button_rect
    global cross_detector_start, cross_detector_end
    button_rect = (0, 0, 0, 0)  # initialized early to avoid NameError
    # Define mouse callback function
    global pelanggar, ids
    
    stream_url, model_name = gui.open_config_gui()

    if not stream_url:
        stream_url = 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8'

    # Open the video stream
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("Error: Could not open the video stream.")
        tk.messagebox.showerror("Stream Error", "Could not open the video stream.")
        exit()

    # model = YOLO('yolov8n.pt') // ini bs diubah-ubah, n = nano, s=small, m=medium, l=large, x=xtra large
    
    model = YOLO(f"{model_name}.pt")  # ex: yolo11n.pt, yolo11x.pt, etc.

    # Load mask
    # mask = cv2.imread('mask_640x360_.png')
    mask = None
    tracker = Sort(max_age=20, min_hits=2, iou_threshold=0.3)
    totalCount = 0
    ids = []

    def draw_line(event, x, y, flags, param):
        global line_points
        global end
        global arrow
        global counter
        global line_points, end, arrow, counter
        global cross_detector_start, cross_detector_end
        
        # On left mouse button click, add point to line_points
        if event == cv2.EVENT_LBUTTONDOWN:            
            counter += 1

            if counter <= 2:
                line_points.append((x, y))
            elif 3 <= counter <= 4:
                end.append((x, y))
            elif counter == 5:
                # Reset everything
                line_points = []
                end = []
                counter = 0
                cross_detector_start = None
                cross_detector_end = None
                print("🧹 Lines cleared.")
                return

            # ✅ Always check and create detectors if two points are available
            if len(line_points) == 2:
                saveToText(line_points=line_points, file_path="start.json")
                cross_detector_start = LineCrossDetector(line_points[0], line_points[1], buffer=15)
                print("✅ cross_detector_start updated")

            if len(end) == 2:
                saveToText(line_points=end, file_path="end.json")
                cross_detector_end = LineCrossDetector(end[0], end[1], buffer=15)
                print("✅ cross_detector_end updated")


    def mouse_click(event, x, y, flags, param):
        global button_rect
        if event == cv2.EVENT_LBUTTONDOWN:
            bx, by, bw, bh = button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                # open_settings_gui()
                print("open setting here")
                setting.open_settings_gui()
            else:
                draw_line(event, x, y, flags, param)  # Let your existing line-drawing continue

    
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_click)
    

    # Setup before while loop
    
    totalCount = 0
    # cross_detector_start = None
    # cross_detector_end = None

    if len(line_points) == 2:
        cross_detector_start = LineCrossDetector(line_points[0], line_points[1], buffer=15)

    if len(end) == 2:
        cross_detector_end = LineCrossDetector(end[0], end[1], buffer=15)
    
    while True:
        success, img = cap.read()
        print(f"Frame shape: {img.shape}")
        
        if not success:
            print(f"[{datetime.now()}] Frame read failed. Trying to reconnect...")
            timesleep = 2 # milliseconds =  2 second
            for attempt in range(5):
                cap.release()
                time.sleep(timesleep)  # Give time before trying again
                cap = cv2.VideoCapture(stream_url)

                if cap.isOpened():
                    print(f"[{datetime.now()}] Reconnected successfully on attempt {attempt + 1}")
                    break
                else:
                    print(f"[{datetime.now()}] Reconnection attempt {attempt + 1} failed...")
                    time.sleep(timesleep)
            # what else below doing ? is it correct ?
            else:
                print(f"[{datetime.now()}] Failed to reconnect after 5 attempts. Exiting...")
                send_message("🚨 SI DILAN: Gagal reconnect CCTV setelah 5 percobaan. Aplikasi dimatikan.")
                break

        # Apply the mask if available
        if mask is not None:
            resized_mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
            masked = cv2.bitwise_and(img, resized_mask)
        else:
            # print("Error: Could not retrieve mask, skipping frame.")
            masked = img

        results = model(masked, stream=True)
        button_rect = (img.shape[1] - 150, 10, 140, 40)  # (x, y, width, height)

        # Draw settings button (top-right corner)
        x, y, w, h = button_rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), cv2.FILLED)
        cv2.putText(img, "Settings", (x + 10, y + 27), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # read content 
        config = setting.load_settings()
        THICKNESS = int(config['thickness'])

        detections = np.empty((0,5))
        detection_classes = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                class_name = model.names[cls]

                # if True:
                known_object = [
                    'car', 'motorcycle', 'bus', 'truck'
                ];

                if class_name in known_object:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil(box.conf[0] * 100)
                    if config.get('show_object_name'):
                        cvzone.putTextRect(img, f'{class_name} {conf}%', (max(0, x1), max(35, y1)), scale=config['scale'], thickness=int(config['thickness']), offset=3)
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currentArray))
                    detection_classes.append(class_name)  # 💡 Save the class

        trackerResults = tracker.update(detections)

        # draw the dot (red )
        for p in line_points:
            cv2.circle(img, p, 5, (0,0,255), cv2.FILLED )
        # draw the second line dot ( yellow )
        for ps in end:
            cv2.circle(img, ps, 5, (0, 255,255), cv2.FILLED )

        # Draw the line if two points are set
        # if len(line_points) == 2:
        #     # cv2.line(img, line_points[0], line_points[1], (0, 0, 255), THICKNESS)
        #     # cross_detector_start = LineCrossDetector(line_points[0], line_points[1])
        #     cross_detector_start.draw_line(img, THICKNESS=THICKNESS)
        
        # if len(end) == 2:
        #     # cv2.line(img, end[0], end[1], (0, 255, 255), THICKNESS)
        #     # cross_detector_end = LineCrossDetector(end[0], end[1])
        #     cross_detector_end.draw_line(img, THICKNESS=THICKNESS)

        # if counter == 4:
        #     cross_detector_start.draw_detection_zone(img)
        #     cross_detector_end.draw_detection_zone(img)
        
        if cross_detector_start:
            cross_detector_start.draw_detection_zone(img)
            cross_detector_start.draw_line(img)
        if cross_detector_end:
            cross_detector_end.draw_detection_zone(img)
            cross_detector_end.draw_line(img)

        for idx,t in enumerate(trackerResults):
            x1, y1, x2, y2, id = t
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2-y1
            id = int(id) + int(latest_id)

            # Match class name based on detection index
            if idx < len(detection_classes):
                class_name = detection_classes[idx]
            else:
                class_name = "unknown"

            if config.get('show_tracker_box'):
                cvzone.cornerRect(img, (x1, y1, w, h), l=3, rt=THICKNESS+2, colorR=(255,0,0))
            if config.get('show_tracker_name'):
                cvzone.putTextRect(img, f'{class_name} with id {id}', (max(0, x1), max(35, y1)), scale=config['scale'], thickness=int(config['thickness']), offset=10 )

            cx, cy = x1+w // 2, y1+h // 2
            currentPoint = (cx, cy)
            current_point = currentPoint
            cv2.circle(img, currentPoint, THICKNESS*2 , (255, 0, 0), cv2.FILLED)

            # Start line crossing
            if cross_detector_start and cross_detector_start.has_crossed(id, current_point):
                ids.append(id)  # track who crossed start
                print(f"Object {id} crossed the START line!")

            # End line crossing
            if cross_detector_end and cross_detector_end.has_crossed(id, current_point):
                if id in ids and id not in pelanggar:
                    pelanggar.append(id)
                    totalCount += 1
                    print(f"Object {id} violated rules!")
                    screenshot_path = f'results/screenshot_{id}.jpg'
                    cv2.imwrite(screenshot_path, img)
                    send_photo(screenshot_path, caption=f"Telah terjadi pelanggaran di {stream_url} dengan id: {id}", cctv=stream_url, object_id=id)

        # Display total count and tracked IDs
        # cvzone.putTextRect(img, f'total: {totalCount} with ids={", ".join(map(str, ids))}', (img.shape[1] - 500, 80), scale=2, thickness=int(config['thickness']), offset=10)
        # cvzone.putTextRect(img, f'Counter: {counter} Start: {str(line_points)} & End: {str(end)}' , ( 10 , 40) , scale=3, thickness=2, offset=15 )
        # cvzone.putTextRect(img, f'total: {totalCount} with ids={", ".join(map(str, ids))}', (30, 80), scale=2, thickness=int(config['thickness']), offset=10)
        if config.get('show_total_pelanggar'):
            cvzone.putTextRect(img, f'total: {totalCount} with pelanggar={", ".join(map(str, pelanggar))}', (30, 120), scale=config['scale'], thickness=int(config['thickness']), offset=10)
        # cvzone.putTextRect(img, f'prev position: {str(previous_positions)}' , ( 10 , 90) , scale=3, thickness=2, offset=15 )
        
        # ini mah buat debuging doang
        # cvzone.putTextRect(img, f'line_point: {line_points} end {end} ', (30, 120), scale=config['scale'], thickness=int(config['thickness']), offset=10)
        if len(ids) > 1000:
            ids = []
        if len(pelanggar) > 1000:
            pelanggar = []
        # Show the result
        cv2.imshow('Image', img)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    # add timestamp to the message
    now = datetime.now()
    print(f"Monitoring stopped at {now}. Total violations: {totalCount}")
    send_message(f"Monitoring stopped at {now}. Total violations: {totalCount}")

if __name__ == "__main__":
    main()