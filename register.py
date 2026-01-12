import cv2
import os

KNOWN_DIR = "known_faces"

if not os.path.exists(KNOWN_DIR):
    os.makedirs(KNOWN_DIR)

name = input("Enter user name: ").strip()
user_path = os.path.join(KNOWN_DIR, name)

if not os.path.exists(user_path):
    os.makedirs(user_path)

cap = cv2.VideoCapture(0)
count = 0

print("Look straight at camera and press 'c' to capture. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    cv2.imshow("Register User", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        count += 1
        img_path = os.path.join(user_path, f"{count}.jpeg")
        cv2.imwrite(img_path, frame)
        print(f"Saved: {img_path}")

        if count >= 10:
            print("Registration complete!")
            break

    elif key == ord('q'):
        print("Registration cancelled")
        break

cap.release()
cv2.destroyAllWindows()
