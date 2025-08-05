from use_pose_detect import detect_pose, start_pose_detection, stop_pose_detection, get_latest_pose, follow_face
import time
from use_drive_controller import drive_controller



if __name__ == "__main__":
    driver = drive_controller()
    driver.stop()
    time.sleep(1)
    print("START in 2 secs")
    start_pose_detection(0.5)
    time.sleep(2)
    for i in range(150):
        follow_face(driver)
#     heads = []
#     for i in range(150):
#         print(i)
#         time.sleep(0.5)
#         try:
#             head = get_latest_pose()["NOSE"]
#         except:
#             head = None
#         print(head)
#         heads.append(head)
#         if head is not None:
#             if head[0] < 1100:
#                 driver.right_step(0.03)
#                 print("RIGHT")
#             if head[0] > 1500:
#                 driver.left_step(0.03)
#                 print("LEFT")
    stop_pose_detection()
