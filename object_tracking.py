import cv2
import numpy as np
from object_detection import ObjectDetection
import math
import time
import matplotlib.pyplot as plt
# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("02.mp4")

# Initialize count
count = 0
frame_count=0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0
# frame_count=0
entry_pos={}
exit_pos={}
h_={}
w_={}

while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        break

    frame_count += 1
    if frame_count % 1 !=0:
        continue


    # Point current frame
    center_points_cur_frame = []

    # Detect objects on frame
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        center_points_cur_frame.append((cx, cy,w,h))
        #print("FRAME N°", count, " ", x, y, w, h)

        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Only at the beginning we compare previous and current frame
    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id += 1
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # Update IDs position
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                    continue

            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)

        # Add new IDs found
        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1

    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt[:2], 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)

    print("Tracking objects")
    print(tracking_objects)
    for key,val in tracking_objects.items():
        if val[1]>670:
            try:
                entry_pos[key]==True
            except:
                entry_pos[key]=count
        if val[1]>680:
            try:
                exit_pos[key]==True
            except:
                exit_pos[key] = count
    print("Entry-Exit Count")
    print(entry_pos)
    print(exit_pos)
    for key,val in tracking_objects.items():
        try:
            h_[key].append(val[3])
        except:
            h_[key]=[val[3]]
        try:
            w_[key].append(val[3])
        except:
            w_[key]=[val[3]]



    print("CUR FRAME LEFT PTS")
    print(center_points_cur_frame)
    #print(pos)
    print("Width")
    print(w_)
    print("Height")
    print(h_)

    cv2.line(frame, (0, 700), (1400, 700), (0, 0, 255), 2)
    cv2.line(frame, (0, 730), (1400, 730), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)

    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27 & 0xFF==ord('d'):
        break
cap.release()
cv2.destroyAllWindows()
for key,val in h_.items():
    plt.plot(h_[key],label=str(key))
plt.show()
