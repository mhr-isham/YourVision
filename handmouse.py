import cv2
import mediapipe as mp
import pyautogui
import warnings
warnings.filterwarnings("ignore")

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
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            screen_x = int(hand_landmarks.landmark[8].x * width)
            screen_y = int(hand_landmarks.landmark[8].y * height)

            curr_x = prev_x + (screen_x - prev_x) / smoothen
            curr_y = prev_y + (screen_y - prev_y) / smoothen

            #pyautogui.moveTo(curr_x, curr_y)

            hand_type = handedness.classification[0].label

            index_folded_ydir = hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y
            middle_folded_ydir = hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y
            ring_folded_ydir = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
            pinky_folded_ydir = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y

            index_folded_xdir = hand_landmarks.landmark[8].x < hand_landmarks.landmark[6].x
            middle_folded_xdir = hand_landmarks.landmark[12].x < hand_landmarks.landmark[10].x
            ring_folded_xdir = hand_landmarks.landmark[16].x < hand_landmarks.landmark[14].x
            pinky_folded_xdir = hand_landmarks.landmark[20].x < hand_landmarks.landmark[18].x

            if hand_type == "Right":
                cv2.putText(frame, "Right Hand detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                thumb_open_ydir = hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y
            else:
                cv2.putText(frame, "Left Hand detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                thumb_open_ydir = hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y

            if index_folded_ydir and middle_folded_ydir and ring_folded_ydir and pinky_folded_ydir and not thumb_open_ydir:
                #pyautogui.click()
                #pyautogui.mouseDown()
                cv2.putText(frame, "Fist=Left click/drag", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  
            else:
                pyautogui.mouseUp() 
            
            if (thumb_open_ydir and index_folded_ydir and middle_folded_ydir and ring_folded and pinky_folded_ydir ):
                #pyautogui.rightClick()
                cv2.putText(frame, "Thumbs Up = Right Click", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    #else:
        #pyautogui.mouseUp()

    cv2.imshow("Hand Mouse(press q to exit, Fist > Left click/drag, Thumbs Up = Right Click)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()