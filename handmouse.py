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
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            screen_x = int(hand_landmarks.landmark[8].x * width)
            screen_y = int(hand_landmarks.landmark[8].y * height)

            curr_x = prev_x + (screen_x - prev_x) / smoothen
            curr_y = prev_y + (screen_y - prev_y) / smoothen

            pyautogui.moveTo(curr_x, curr_y)

            hand_type = handedness.classification[0].label
            prev_x, prev_y = curr_x, curr_y


            #4 fingers y directions fold
            index_folded_ydir = hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y
            middle_folded_ydir = hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y
            ring_folded_ydir = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
            pinky_folded_ydir = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
            thumb_open_ydir = hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y

            #hand detection and thumb open y direction
            if hand_type == "Right":
                cv2.putText(frame, "Right Hand detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                index_folded_xdir = hand_landmarks.landmark[8].x > hand_landmarks.landmark[6].x
                middle_folded_xdir = hand_landmarks.landmark[12].x > hand_landmarks.landmark[10].x
                ring_folded_xdir = hand_landmarks.landmark[16].x > hand_landmarks.landmark[14].x
                pinky_folded_xdir = hand_landmarks.landmark[20].x > hand_landmarks.landmark[18].x
                
            else:
                cv2.putText(frame, "Left Hand detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                index_folded_xdir = hand_landmarks.landmark[8].x < hand_landmarks.landmark[6].x
                middle_folded_xdir = hand_landmarks.landmark[12].x < hand_landmarks.landmark[10].x
                ring_folded_xdir = hand_landmarks.landmark[16].x < hand_landmarks.landmark[14].x
                pinky_folded_xdir = hand_landmarks.landmark[20].x < hand_landmarks.landmark[18].x

            '''
            Test back side and palm side


        
            gesture_state = {
                "thumb_open_ydir": False,
                "index_folded_xdir": False,
                "index_folded_ydir": False,
                "middle_folded_xdir": False,
                "middle_folded_ydir": False,
                "ring_folded_xdir": False,
                "ring_folded_ydir": False,
                "pinky_folded_xdir": False,
                "pinky_folded_ydir": False
            }

           
            def check_and_print(gesture_name, condition, message):
                if condition and not gesture_state[gesture_name]:
                    print(message)
                    gesture_state[gesture_name] = True
                elif not condition:
                    gesture_state[gesture_name] = False


            check_and_print("thumb_open_ydir", thumb_open_ydir, "Thumb open")
            check_and_print("index_folded_xdir", index_folded_xdir, "Index folded - X dir")
            check_and_print("index_folded_ydir", index_folded_ydir, "Index folded - Y dir")
            check_and_print("middle_folded_xdir", middle_folded_xdir, "Middle folded - X dir")
            check_and_print("middle_folded_ydir", middle_folded_ydir, "Middle folded - Y dir")
            check_and_print("ring_folded_xdir", ring_folded_xdir, "Ring folded - X dir")
            check_and_print("ring_folded_ydir", ring_folded_ydir, "Ring folded - Y dir")
            check_and_print("pinky_folded_xdir", pinky_folded_xdir, "Pinky folded - X dir")
            check_and_print("pinky_folded_ydir", pinky_folded_ydir, "Pinky folded - Y dir")  
            
            # Determine if palm or back of hand is facing the camera
            wrist_z = hand_landmarks.landmark[0].z
            fingertips = [8, 12, 16, 20]  # index, middle, ring, pinky tips
            avg_tip_z = sum(hand_landmarks.landmark[i].z for i in fingertips) / len(fingertips)

            if avg_tip_z < wrist_z:
                hand_side = "Palm facing camera"
            else:
                hand_side = "Back of hand facing camera"

            print(handedness.classification[0].label, hand_side)
            '''

            

            # LEFT CLICK
            if index_folded_ydir and middle_folded_ydir and ring_folded_ydir and pinky_folded_ydir:
                pyautogui.click()
                pyautogui.mouseDown()
                cv2.putText(frame, "Fist=Left click/drag", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  
            else:
                pyautogui.mouseUp() 
            
            # RIGHT CLICK
            if (thumb_open_ydir and index_folded_xdir and middle_folded_xdir and ring_folded_xdir and pinky_folded_xdir ):
                pyautogui.mouseUp()
                pyautogui.rightClick()
                cv2.putText(frame, "Thumbs Up = Right Click", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                

    else:
        pyautogui.mouseUp()

    cv2.imshow("Hand Mouse(press q to exit, Fist > Left click/drag, Thumbs Up = Right Click)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()