import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

Cam_index = input("Enter camera index (default is 0): ")

width, height = pyautogui.size()

cap = cv2.VideoCapture(int(Cam_index) if Cam_index.isdigit() else 0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame from camera. Try changing camera index. Exiting...")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            screen_x = int(hand_landmarks.landmark[8].x * width)
            screen_y = int(hand_landmarks.landmark[8].y * height)

            pyautogui.moveTo(screen_x, screen_y)

            if hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y \
                and hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y:
                    pyautogui.mouseDown()  
            else:
                pyautogui.mouseUp() 


    cv2.imshow("Hand Mouse(press q to exit)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()