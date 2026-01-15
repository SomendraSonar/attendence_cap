import cv2
import os

KNOWN_DIR = "known_faces"

if not os.path.exists(KNOWN_DIR):
    os.makedirs(KNOWN_DIR)

name = input("Enter user name: ").strip()
user_folder = os.path.join(KNOWN_DIR, name)

os.makedirs(user_folder, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Press 'c' to capture image")

while count < 10:
    ret, frame = cap.read()
    cv2.imshow("Register User", frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        count += 1
        cv2.imwrite(f"{user_folder}/{count}.jpeg", frame)
        print(f"Captured {count}/10")

cap.release()
cv2.destroyAllWindows()
print("Registration completed!")
