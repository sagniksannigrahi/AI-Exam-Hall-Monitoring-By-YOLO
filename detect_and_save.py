from ultralytics import YOLO
import cv2
import sqlite3
from datetime import datetime

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

def save_to_db(count):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("INSERT INTO attendance (date, persons_detected) VALUES (?,?)",
                   (date, count))
    
    conn.commit()
    conn.close()
    print("Attendance saved in database")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)

    person_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if model.names[cls] == "person":
                person_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

    cv2.putText(frame, f"Persons: {person_count}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,0,255), 2)

    cv2.putText(frame, "Press 'S' to Save Attendance",
                (20,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255,255,0), 2)

    cv2.imshow("YOLO Smart Attendance", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):   # Save attendance
        save_to_db(person_count)

    if key == ord('q'):   # Quit
        break

cap.release()
cv2.destroyAllWindows()
