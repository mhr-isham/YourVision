import cv2
import mediapipe as mp
import numpy as np
import datetime



is_recording = False
video_writer = None
camera_index = input("Enter camera index (default is 0): ")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

pose = mp_pose.Pose()
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(int(camera_index) if camera_index.isdigit() else 0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame from camera. Try changing camera index. Exiting...")
        break
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)
    hand_results = hands.process(rgb)

    stickman = 255 * np.ones_like(frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
        )

        landmarks = results.pose_landmarks.landmark
        points={}
        for idx, landmark in enumerate(landmarks):
            points[idx] = (int(landmark.x * width), int(landmark.y * height))

        # circle head
        nose_x, nose_y = points[mp_pose.PoseLandmark.NOSE]
        head_radius = int(0.1 * height)  
        cv2.circle(stickman, (nose_x, nose_y), head_radius, (0,0,0), 2)  


        connections = [

            #Hands and Arms
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER),
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
            (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
            (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
            (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),


            # Torso
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
            (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP),
            (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP),


            # Legs
            (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
            (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
            (mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.LEFT_HEEL),
            (mp_pose.PoseLandmark.LEFT_HEEL, mp_pose.PoseLandmark.LEFT_FOOT_INDEX),
            (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
            (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE),
            (mp_pose.PoseLandmark.RIGHT_ANKLE, mp_pose.PoseLandmark.RIGHT_HEEL),
            (mp_pose.PoseLandmark.RIGHT_HEEL, mp_pose.PoseLandmark.RIGHT_FOOT_INDEX),
]

        for connection in connections:
            start, end = connection
            start, end = int(start.value), int(end.value)
            if start in points and end in points:
                cv2.line(stickman, points[start], points[end], (0, 0, 0), 3)
        
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            for connection in mp_hands.HAND_CONNECTIONS:
                start = hand_landmarks.landmark[connection[0]]
                end = hand_landmarks.landmark[connection[1]]
                start_point = (int(start.x * width), int(start.y * height))
                end_point = (int(end.x * width), int(end.y * height))
                cv2.line(stickman, start_point, end_point, (0, 0, 0), 2)

    cv2.imshow('Dance with Me - Original(PRESS q TO EXIT)', frame)
    cv2.imshow("Dance with Me - Stickman(PRESS 's' for a snapshot, 'r' to record)", stickman)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Press 's' to save a snapshot
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'dancewithme_snapshot_{timestamp}.png'
        cv2.imwrite(filename, stickman)
        print(f"Snapshot saved as '{filename}'")

    if key == ord('r'):  # Press 'r' to start/stop recording
        if not is_recording:
            #Start Recording
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename=f'dancewithme_recording_{timestamp}.avi'
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
            is_recording = True
            print("Recording started...")

        else:
            #Stop Recording
            is_recording = False
            video_writer.release()
            video_writer = None
            print("Recording stopped.")

    if is_recording and video_writer is not None:
        video_writer.write(stickman)

    if key == ord('q'):  # Press 'q' to exit
        if is_recording:
            video_writer.release() #Save recording before closing
        break

cap.release()
cv2.destroyAllWindows()