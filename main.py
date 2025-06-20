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
from bot import send_photo
import setting

# global var
# Line drawing variables
line_points =  load("start.json")# Store the points of the line
end =  load("end.json")# Store the points of the line
arrow = load("arrow.json")
counter = len(line_points) + len(end)
ids = []
pelanggar = []

# root = tk.Tk()
# root.withdraw()  # Hide main window
# stream_url = simpledialog.askstring("Input", "Enter CCTV link (leave blank for default):")

# URL of the HLS stream
# stream_url = 'https://cctv.purwakartakab.go.id/cctv/rel-munjul.m3u8?v=4066696'  # Example stream URL

# stream_url = 'https://s3klari.qumicon.info:8888/camFix-F2/stream.m3u8' #klari arah cikampek
# stream_url = 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8' #klari ke arah pintu toll kartim
# stream_url = 'https://s3klari.qumicon.info:8888/camFix-F1/stream.m3u8' #klari arah karawang

# I want to use gui on test.py to use as stream_url, how do i do that ?

# stream_url = input("input link cctv: (enter untuk menggunakan link default)")  # Example stream URL



        
def main():
    global button_rect
    button_rect = (0, 0, 0, 0)  # initialized early to avoid NameError
    # Define mouse callback function
    
    stream_url = gui.open_config_gui()

    if not stream_url:
        stream_url = 'https://s3klari.qumicon.info:8888/camFix-F3/stream.m3u8'

    # Open the video stream
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("Error: Could not open the video stream.")
        tk.messagebox.showerror("Stream Error", "Could not open the video stream.")
        exit()

    # model = YOLO('yolov8n.pt')
    model = YOLO('yolo11n.pt')

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
        
        # On left mouse button click, add point to line_points
        if event == cv2.EVENT_LBUTTONDOWN:
            counter+=1

            if counter <= 2:
                line_points.append((x, y))
                if len(line_points) == 2:
                    saveToText(line_points=line_points, file_path="start.json")
            
            elif 3 <= counter <= 4:
                end.append((x, y))
                if len(end) == 2:
                    saveToText(line_points=end, file_path="end.json")
            
            if counter == 5:
                # Reset after the fifth click
                line_points = []
                end = []
                counter = 0


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
    

    

    while True:
        success, img = cap.read()
        if not success:
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
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                class_name = model.names[cls]

                if True:
                # if class_name == 'car' or class_name == 'motorcycle':
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    conf = math.ceil(box.conf[0] * 100)
                    if config.get('show_object_name'):
                        cvzone.putTextRect(img, f'{class_name} {conf}%', (max(0, x1), max(35, y1)), scale=config['scale'], thickness=int(config['thickness']), offset=3)
                    currentArray = np.array([x1, y1, x2, y2, conf])
                    detections = np.vstack((detections, currentArray))

        trackerResults = tracker.update(detections)

        for p in line_points:
            cv2.circle(img, p, 10, (0,0,150), cv2.FILLED )
        
        for ps in end:
            cv2.circle(img, ps, 5, (0, 255,255), cv2.FILLED )

        # Draw the line if two points are set
        if len(line_points) == 2:
            cv2.line(img, line_points[0], line_points[1], (0, 0, 255), 3)
        
        if len(end) == 2:
            cv2.line(img, end[0], end[1], (0, 255, 255), 3)

        # Track previous positions of each object by ID
        previous_positions = {}
        

        for t in trackerResults:
            x1, y1, x2, y2, id = t
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2-y1
            id = int(id)
            if config.get('show_tracker_box'):
                cvzone.cornerRect(img, (x1, y1, w, h), l=3, rt=THICKNESS+2, colorR=(255,0,0))
            if config.get('show_tracker_name'):
                cvzone.putTextRect(img, f'{class_name} with id {id}', (max(0, x1), max(35, y1)), scale=config['scale'], thickness=int(config['thickness']), offset=10 )

            cx, cy = x1+w // 2, y1+h // 2
            currentPoint = (cx, cy)
            point = cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            # if point cross the line, count it
            if len(line_points) == 2:
                # current_side = is_above_line(currentPoint, line_points[0], line_points[1])

                # Check if we have a previous position for this object
                    # If the signs of `current_side` and `previous_side` are different, the object has crossed the line
                    # if current_side * previous_side < 0:
                start1 = line_points[0]
                start2 = line_points[1]
                if start1[0] < cx < start2[0] and start1[1] - 20 < cy < start2[1] + 20:
                    if ids.count(id) == 0:
                        # totalCount += 1  # Increment the counter
                        ids.append(id)
                        # capture the screenshoot of img
                        # screenshot_path = f'results/screenshot_{id}.jpg'  # Generate a unique filename based on the id
                        # cv2.imwrite(screenshot_path, img)

            if len(end) == 2:
                # disini cek apa cross yang end
                start1 = end[0]
                start2 = end[1]
                if start1[0] < cx < start2[0] and start1[1] - 20 < cy < start2[1] + 20:
                    # check id ini udah ada yg input sebelumnya, yaitu start
                    if ids.count(id) > 0:
                        if pelanggar.count(id) == 0:
                            totalCount += 1  # Increment the counter
                            pelanggar.append(id)
                            # ids.append(id)
                            # capture the screenshoot of img
                            screenshot_path = f'results/screenshot_{id}.jpg'  # Generate a unique filename based on the id
                            cv2.imwrite(screenshot_path, img)
                            # Send it via Telegram
                            send_photo(screenshot_path, caption=f"Detected event ID: {id}")

        # Display total count and tracked IDs
        # cvzone.putTextRect(img, f'total: {totalCount} with ids={", ".join(map(str, ids))}', (img.shape[1] - 500, 80), scale=2, thickness=int(config['thickness']), offset=10)
        # cvzone.putTextRect(img, f'Counter: {counter} Start: {str(line_points)} & End: {str(end)}' , ( 10 , 40) , scale=3, thickness=2, offset=15 )
        # cvzone.putTextRect(img, f'total: {totalCount} with ids={", ".join(map(str, ids))}', (30, 80), scale=2, thickness=int(config['thickness']), offset=10)
        cvzone.putTextRect(img, f'total: {totalCount} with pelanggar={", ".join(map(str, pelanggar))}', (30, 120), scale=config['scale'], thickness=int(config['thickness']), offset=10)
        # cvzone.putTextRect(img, f'prev position: {str(previous_positions)}' , ( 10 , 90) , scale=3, thickness=2, offset=15 )
        # Show the result
        cv2.imshow('Image', img)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()