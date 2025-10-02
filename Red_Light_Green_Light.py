import cv2
import mediapipe as mp
import time
import random

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

camera_index = input("Enter camera index (default is 0): ")
cap = cv2.VideoCapture(int(camera_index) if camera_index.isdigit() else 0)

level = 1
time_limit = 60  
threshold = 100   
freeze_active = False
freeze_start = 0
freeze_duration = 2

game_over = False
message = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    if not game_over:
        if 'level_start_time' not in locals():
            level_start_time = time.time()
            left_knee_start, right_knee_start = None, None
            max_movement = 0
            freeze_active = False
            freeze_count = random.randint(1, 3)
            freeze_times = sorted([random.uniform(2, time_limit - 2) for _ in range(freeze_count)])
            freeze_index = 0

        elapsed = time.time() - level_start_time
        remaining = max(0, int(time_limit - elapsed))
        cv2.putText(frame, f"Level {level} | Time: {remaining}s | Threshold: {threshold}", 
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        circle_color = (0, 255, 0)
        if freeze_active:
            circle_color = (0, 0, 255)
        cv2.circle(frame, (w-80, 80), 40, circle_color, -1)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            left_knee = (int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * w),
                         int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * h))
            right_knee = (int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x * w),
                          int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y * h))

            cv2.circle(frame, left_knee, 10, (0, 255, 0), -1)
            cv2.circle(frame, right_knee, 10, (0, 0, 255), -1)

            if left_knee_start is None:
                left_knee_start, right_knee_start = left_knee[0], right_knee[0]

            movement = abs(left_knee[0] - left_knee_start) + abs(right_knee[0] - right_knee_start)
            max_movement = max(max_movement, movement)

            progress_ratio = min(max_movement / threshold, 1.0)
            bar_width = int(progress_ratio * w)
            cv2.rectangle(frame, (0, h-30), (bar_width, h), (0, 255, 0), -1)
            cv2.rectangle(frame, (0, h-30), (w, h), (0, 255, 0), 2)  # outline

            if freeze_active:
                if abs(left_knee[0] - left_knee_start) > 12 or abs(right_knee[0] - right_knee_start) > 12:
                    message = "Moved during freeze! Game Over."
                    game_over = True
                if time.time() - freeze_start > freeze_duration:
                    freeze_active = False
                    left_knee_start, right_knee_start = left_knee[0], right_knee[0]
                    message = "Freeze over, keep moving!"
            else:
                if freeze_index < len(freeze_times) and elapsed >= freeze_times[freeze_index]:
                    freeze_active = True
                    freeze_start = time.time()
                    freeze_index += 1
                    message = "Freeze! Stay still!"

        if elapsed >= time_limit and not freeze_active:
            if max_movement >= threshold:
                level += 1
                time_limit = max(5, time_limit - 1)   
                threshold += 20                    
                message = f"Level Up! Now Level {level}"
                level_start_time = time.time()
                left_knee_start, right_knee_start = None, None
                max_movement = 0
            else:
                message = "Ran out of time! Game Over."
                game_over = True

    if message:
        cv2.putText(frame, message, (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.9, (0, 255, 255) if "Up" in message else (0, 0, 255), 2)

    cv2.imshow("Red Light Green Light", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if game_over:
        cv2.imshow("Red Light Green Light", frame)
        cv2.waitKey(3000)
        break

cap.release()
cv2.destroyAllWindows()

