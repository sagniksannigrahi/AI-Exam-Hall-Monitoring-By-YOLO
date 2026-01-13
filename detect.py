from ultralytics import YOLO
import cv2

# Load YOLOv8 nano model (fast for webcam)
model = YOLO("yolov8n.pt")

# Open webcam (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Webcam not found")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO on frame
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

    cv2.imshow("YOLO Smart Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
