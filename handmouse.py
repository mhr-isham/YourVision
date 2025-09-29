import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

Cam_index = input("Enter camera index (default is 0): ")
prev_x, prev_y = 0, 0
smoothen = 5
width, height = pyautogui.size()

cap = cv2.VideoCapture(int(Cam_index) if Cam_index.isdigit() else 0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame from camera. Try changing camera index. Exiting...")
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            screen_x = int(hand_landmarks.landmark[8].x * width)
            screen_y = int(hand_landmarks.landmark[8].y * height)

            curr_x = prev_x + (screen_x - prev_x) / smoothen
            curr_y = prev_y + (screen_y - prev_y) / smoothen

            pyautogui.moveTo(curr_x, curr_y)

            if hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y \
                and hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y:
                    pyautogui.click()
                    pyautogui.mouseDown()

                    cv2.putText(frame, "Fist=Left click/drag", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  
            else:
                pyautogui.mouseUp() 
            
            if (hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y and
                hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y and
                hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y and
                hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y and
                hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y):
                pyautogui.rightClick()
                cv2.putText(frame, "Thumbs Up = Right Click", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    else:
        pyautogui.mouseUp()

    cv2.imshow("Hand Mouse(press q to exit, Fist > Left click/drag, Thumbs Up = Right Click)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()