

import threading
import time
from noahs_pose_detector import PoseDetector
from use_camera import capture_photo, capture_photo_bytes

pose_detector = PoseDetector()
LATEST_POSE = None
_pose_thread = None
_stop_event = threading.Event()

def detect_pose():
    global LATEST_POSE
    b = capture_photo_bytes()
    points = pose_detector.get_pose_points(b)
    LATEST_POSE = points
    return points

def _pose_detection_loop(interval=0.5):
    while not _stop_event.is_set():
        detect_pose()
        time.sleep(interval)

def start_pose_detection(interval=0.5):
    global _pose_thread, _stop_event
    if _pose_thread is None or not _pose_thread.is_alive():
        _stop_event.clear()
        _pose_thread = threading.Thread(target=_pose_detection_loop, args=(interval,))
        _pose_thread.daemon = True  # Optional: allows thread to exit when main thread exits
        _pose_thread.start()
        print("Pose detection started.")
    else:
        print("Pose detection is already running.")

def stop_pose_detection():
    global _stop_event
    if _pose_thread and _pose_thread.is_alive():
        _stop_event.set()
        _pose_thread.join()
        print("Pose detection stopped.")
    else:
        print("Pose detection is not running.")




def get_latest_pose():
    return LATEST_POSE




def follow_face(driver, interval=0.5, speed=0.03, right_bound=1100, left_bound=1500):
    time.sleep(interval)
    try:
        head = get_latest_pose()["NOSE"]
    except:
        head = None
    if head is not None:
        if head[0] < right_bound:
            driver.right_step(speed)
        if head[0] > left_bound:
            driver.left_step(speed)


if __name__ == "__main__":
    time.sleep(3)
    print("START in 2 secs")
    time.sleep(2)
    start_pose_detection()
    heads = []
    for i in range(30):
        time.sleep(0.5)
        try:
            head = get_latest_pose()["LEFT_WRIST"]
        except:
            head = None
        print(head)
        heads.append(head)
    stop_pose_detection()



