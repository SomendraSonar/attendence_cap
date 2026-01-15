# from main import recognize_face
# from deepface import DeepFace

# print("Loading model...")
# model = DeepFace.build_model("ArcFace")
# print("Model loaded!")

# user = recognize_face(model)
# print("Recognized:", user)


import cv2
v = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, frame = v.read()
print("OK" if ret else "FAIL")
