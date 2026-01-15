# face_worker.py

from scan_state import scan_status
from main import recognize_face

def run_face_scan():
    scan_status["running"] = True
    scan_status["done"] = False
    scan_status["user"] = None

    user = recognize_face()

    scan_status["user"] = user or "unknown"
    scan_status["done"] = True
    scan_status["running"] = False
