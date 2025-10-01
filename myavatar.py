import  cv2

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
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=7)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    stylized = cv2.stylization(frame, sigma_s=250, sigma_r=0.75)

    # Compare both functions
    cv2.imshow("Cartoon", cartoon)
    cv2.imshow("Stylized-opencv", stylized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()