import cv2
import mediapipe as mp
import random
import time

camera_index = input("Enter camera index (default is 0): ")
cap = cv2.VideoCapture(int(camera_index) if camera_index.isdigit() else 0)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, refine_landmarks=True)

open_mouth = False
score=0
lives = 3
speed = 5
food_x, food_y = None, None
food_visible = False
cv2.namedWindow("Food Eater Game")

while True:
    ret, frame = cap.read()
    if not ret or not cap.isOpened():
        print("Failed to get camera. Try changing camera index. Exiting...")
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)


     if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get mouth landmarks
            upper_lip = face_landmarks.landmark[13]  # Upper lip
            lower_lip = face_landmarks.landmark[14]  # Lower lip

            # Convert normalized coordinates to pixel coordinates
            mouth_open_val = abs(upper_lip.y - lower_lip.y) * h
            mouth_open = mouth_open_val > 15

            if not food_visible:
                food_x = random.randint(50, w-50)
                food_y = h - 10
                food_visible = True

            if food_visible:
                food_y -= speed
                cv2.circle(frame, (food_x, food_y), 15, (0,0,255), -1)

                if mouth_x and mouth_y and mouth_open:
                    if (abs(food_x - mouth_x) < 30) and (abs(food_y - mouth_y) < 30):
                        score += 1
                        speed += 1   # increase difficulty
                        food_on_screen = False

                if food_y < 0:
                    lives -= 1
                    food_on_screen = False
            
            cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Lives: {lives}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if lives <= 0:
                cv2.putText(frame, "Game Over!", (200, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                cv2.imshow("Food Eater", frame)
                cv2.waitKey(5000)
                break

            cv2.imshow("Food Eater", frame)

             if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()