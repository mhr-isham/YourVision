import  cv2
import datetime

camera_index=input("Enter camera index (default is 0): ")

cap = cv2.VideoCapture(int(camera_index) if camera_index.isdigit() else 0)
print("press 'q' to quit")
while True:
    ret, frame = cap.read()
    if not ret or not cap.isOpened():
        print("Failed to get camera. Try changing camera index. Exiting...")
        break
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)
    color = cv2.bilateralFilter(frame, d=9, sigmaColor=200, sigmaSpace=200)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=11, C=8)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    stylized = cv2.stylization(frame, sigma_s=270, sigma_r=0.55)

    # Two versions of avatar
    cv2.imshow("Avatar version 1 - Cartoonized", cartoon)
    cv2.imshow("Avatar version 2 - Stylized", stylized)

    key =cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'cartoon_avatar_{timestamp}.png'
        cv2.imwrite(filename, cartoon)
        print(f"Avatar version 1 - Cartoonized version saved as '{filename}'")
    elif key == ord('c'):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'stylized_avatar_{timestamp}.png'
        cv2.imwrite(filename, stylized)
        print("Avatar version 2 - Stylized version saved as '{filename}'")

cap.release()
cv2.destroyAllWindows()
