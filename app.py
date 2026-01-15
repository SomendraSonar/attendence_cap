# from flask import Flask, render_template, request
# from datetime import datetime
# from deepface import DeepFace
# import os
# import time
# from main import recognize_face, register_user

# app = Flask(__name__)

# ATTENDANCE_FILE = "attendance.csv"
# KNOWN_DIR = os.path.join(os.path.dirname(__file__), "known_faces")

# print("\n=====================================")
# print("Loading ArcFace model... Please wait...")
# model = DeepFace.build_model("ArcFace")
# print("Model loaded successfully!")
# print("=====================================\n")


# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/register")
# def register_page():
#     return render_template("register.html")


# @app.route("/do_register", methods=["POST"])
# def do_register():
#     username = request.form.get("username")

#     if not username:
#         return render_template("login_failed.html", message="Username required")

#     register_user(username)
#     return render_template("login_success.html", user=username)


# @app.route("/login")
# def login_page():
#     return render_template("login.html")


# @app.route("/do_login", methods=["POST"])
# def do_login():
#     if not os.path.exists(KNOWN_DIR) or len(os.listdir(KNOWN_DIR)) == 0:
#         return render_template("login_failed.html", message="No registered users found!")

#     print("Capturing frames... Look at the camera")
#     time.sleep(1)

#     user = recognize_face(model)

#     if user:
#         mark_attendance(user)
#         return render_template("login_success.html", user=user)

#     return render_template("login_failed.html", message="Face not recognized!")


# @app.route("/attendance")
# def show_attendance():
#     records = []

#     if os.path.exists(ATTENDANCE_FILE):
#         with open(ATTENDANCE_FILE) as f:
#             for line in f:
#                 records.append(line.strip().split(","))

#     return render_template("attendence.html", rows=records)


# def mark_attendance(user):
#     now = datetime.now()
#     with open(ATTENDANCE_FILE, "a") as f:
#         f.write(f"{user},{now.date()},{now.strftime('%H:%M:%S')}\n")


# if __name__ == "__main__":
#     app.run(debug=False)






from flask import Flask, render_template, request, jsonify
import threading
from datetime import datetime
from face_worker import run_face_scan
from scan_state import scan_status

app = Flask(__name__)
ATTENDANCE_FILE = "attendance.csv"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/start_scan", methods=["POST"])
def start_scan():
    if not scan_status["running"]:
        t = threading.Thread(target=run_face_scan)
        t.start()
    return jsonify({"started": True})

@app.route("/scan_status")
def status():
    return jsonify({
        "running": scan_status["running"],
        "done": scan_status["done"],
        "user": scan_status["user"]
    })

@app.route("/login_success")
def login_success():
    user = request.args.get("user")
    mark_attendance(user)
    return render_template("login_success.html", user=user)

@app.route("/login_failed")
def login_failed():
    msg = request.args.get("msg", "Login Failed")
    return render_template("login_failed.html", message=msg)

@app.route("/attendance")
def attendance():
    rows = []
    try:
        with open(ATTENDANCE_FILE) as f:
            for line in f:
                rows.append(line.strip().split(","))
    except: pass
    return render_template("attendance.html", rows=rows)

def mark_attendance(user):
    now = datetime.now()
    with open(ATTENDANCE_FILE, "a") as f:
        f.write(f"{user},{now.date()},{now.strftime('%H:%M:%S')}\n")

if __name__ == "__main__":
    app.run(debug=False)
