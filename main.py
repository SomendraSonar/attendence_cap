import os
import cv2
from deepface import DeepFace
import pandas as pd
from datetime import datetime

KNOWN_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.csv"

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    df = pd.DataFrame([[name, date, time]], columns=["Name", "Date", "Time"])
    df.to_csv(ATTENDANCE_FILE, mode='a', header=not os.path.exists(ATTENDANCE_FILE), index=False)

    print(f"Attendance Marked: {name}")

cap = cv2.VideoCapture(0)
print("Look at camera to mark attendance...")

while True:
    ret, frame = cap.read()
    cv2.imshow("Attendance", frame)

    for user in os.listdir(KNOWN_DIR):
        user_path = os.path.join(KNOWN_DIR, user)

        result = DeepFace.verify(frame, os.path.join(user_path, os.listdir(user_path)[0]), model_name='ArcFace', enforce_detection=False)

        if result['distance'] < 0.45:  # threshold
            mark_attendance(user)
            cap.release()
            cv2.destroyAllWindows()
            exit()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
