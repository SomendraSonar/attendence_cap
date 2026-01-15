# import os
# import cv2
# from deepface import DeepFace

# # IMPORTANT: point to absolute path
# KNOWN_DIR = os.path.join(os.path.dirname(__file__), "known_faces")

# def register_user(username):
#     user_path = os.path.join(KNOWN_DIR, username)
#     os.makedirs(user_path, exist_ok=True)

#     cap = cv2.VideoCapture(0)
#     count = 0
#     print(f"Registering {username}...")

#     while count < 10:
#         ret, frame = cap.read()
#         cv2.imwrite(os.path.join(user_path, f"{count}.jpeg"), frame)
#         print(f"Captured {count+1}/10")
#         count += 1
#         cv2.waitKey(300)

#     cap.release()
#     cv2.destroyAllWindows()
#     print("Registration Complete!")


# def recognize_face(model=None):
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     cap.release()

#     if not ret:
#         print("Camera failed!")
#         return None

#     print("Checking faces...")

#     if not os.path.exists(KNOWN_DIR) or len(os.listdir(KNOWN_DIR)) == 0:
#         print("No registered users")
#         return None

#     best_user = None
#     best_distance = 0.55  # threshold for ArcFace
#     print("Known users:", os.listdir(KNOWN_DIR))

#     for uname in os.listdir(KNOWN_DIR):
#         user_folder = os.path.join(KNOWN_DIR, uname)

#         for img in os.listdir(user_folder):
#             img_path = os.path.join(user_folder, img)

#             try:
#                 result = DeepFace.verify(
#                     frame,
#                     img_path,
#                     model_name="ArcFace",
#                     enforce_detection=False
#                 )

#                 dist = result["distance"]
#                 print(f"{uname} -> {dist}")

#                 if dist < best_distance:
#                     best_distance = dist
#                     best_user = uname

#             except Exception as e:
#                 print("Error comparing:", e)

#     print("BEST MATCH:", best_user, "FINAL DISTANCE:", best_distance)
#     return best_user


# main.py

import os
import cv2
import time
from deepface import DeepFace

KNOWN_DIR = os.path.join(os.path.dirname(__file__), "known_faces")
THRESHOLD = 0.55
MARGIN = 0.10
MAX_FRAMES = 10
VOTE_REQUIRED = 7

def recognize_face():
    if not os.path.exists(KNOWN_DIR) or len(os.listdir(KNOWN_DIR)) == 0:
        print("ERROR: No registered users in known_faces")
        return None

    print("\nRegistered users:", os.listdir(KNOWN_DIR))
    print("\nDetecting face... Look at the camera\n")

    cap = cv2.VideoCapture(0)
    time.sleep(0.5)

    votes = []
    frame_count = 0

    while frame_count < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Face Login", frame)
        cv2.waitKey(1)

        frame_count += 1

        best_user = None
        best_dist = 999
        second_best = 999

        for uname in os.listdir(KNOWN_DIR):
            udir = os.path.join(KNOWN_DIR, uname)

            for img in os.listdir(udir):
                path = os.path.join(udir, img)

                try:
                    r = DeepFace.verify(
                        frame,
                        path,
                        model_name="ArcFace",
                        detector_backend="retinaface",
                        enforce_detection=False
                    )

                    dist = r["distance"]

                    if dist < best_dist:
                        second_best = best_dist
                        best_dist = dist
                        best_user = uname
                    elif dist < second_best:
                        second_best = dist

                except Exception as e:
                    print("DeepFace error:", e)

        print(f"[Frame {frame_count}] best={best_user} dist={best_dist:.4f} 2nd={second_best:.4f}")

        if best_user and best_dist < THRESHOLD and (second_best - best_dist) > MARGIN:
            votes.append(best_user)
        else:
            votes.append("unknown")

        if votes.count(best_user) >= VOTE_REQUIRED:
            break

    cap.release()
    cv2.destroyAllWindows()

    winner = max(set(votes), key=votes.count)
    count = votes.count(winner)

    if winner != "unknown" and count >= VOTE_REQUIRED:
        print(f"\n✔ FINAL USER = {winner}  ({count}/{frame_count})")
        return winner

    print("\n✖ FINAL USER = UNKNOWN")
    return None
