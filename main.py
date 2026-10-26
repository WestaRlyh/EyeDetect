from pygaze import PyGaze, PyGazeRenderer
import cv2
import time
import numpy as np
from gaze_tracking import GazeTracking
import threading

# 初始化眼睛对象
eye = GazeTracking()
blink_offset_threshold = 10
blink_count = 0

# 设定注视点偏移警告的阈值时间（秒）
warning_time_threshold = 5
gaze_offset_time = 0
Offset_Threshold = 10#眼球居中偏移量

pg = PyGaze()
pgren = PyGazeRenderer()
cap = cv2.VideoCapture(0)  # 0 is the default camera

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gaze_result = pg.predict(frame)
        for face in gaze_result:
            print(f"Face bounding box: {face.bbox}")
            pitch, yaw, roll = face.get_head_angles()   #头部姿态的旋转向量中计算头部姿态的欧拉角
            g_pitch, g_yaw = face.get_gaze_angles()     #计算眼睛的注视角度
            print(f"Face angles: pitch={pitch}, yaw={yaw}, roll={roll}.")
            print(f"Distance to camera: {face.distance}")
            print(f"Gaze angles: pitch={g_pitch}, yaw={g_yaw}")
            print(f"Gaze vector: {face.gaze_vector}")
            print(f"Looking at camera: {pg.look_at_camera(face)}")

            #增加关注偏移提醒
            if abs(g_pitch) > Offset_Threshold or abs(g_yaw) > Offset_Threshold:
                gaze_offset_time += 1/30  # 时间增加，假设摄像头帧率为30fps
            else:
                gaze_offset_time = 0
            if gaze_offset_time >= warning_time_threshold:
                print("WARNING: Gaze point has been off center for too long!")


            pgren.render(frame, face, draw_face_bbox=True, draw_face_landmarks=False, draw_3dface_model=False,draw_head_pose=False, draw_gaze_vector=True)
            if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                cv2.imshow("Face", frame)
            else:
                print("Invalid image")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


finally:
    cap.release()
    cv2.destroyAllWindows()
    