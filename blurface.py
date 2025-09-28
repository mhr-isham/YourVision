import cv2
import numpy as np
import time

CAM_INDEX = 0  # Change this if you have multiple cameras
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
SCALE_FACTOR = 1.1
BLUR_TYPE = 'Gaus'
PIXELATE_BLOCK_SIZE = 20
GAUSSIAN_KERNEL_SIZE = (35, 35)
SHOW_DETECTION_RECT=False


cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    raise RuntimeError(f'Failed to load cascade at {cascade_path}')

def apply_blur(roi, ksize=GAUSSIAN_KERNEL_SIZE):
    kx, ky = ksize
    kx = kx + 1 if kx % 2 == 0 else kx
    ky = ky + 1 if ky % 2 == 0 else ky
    return cv2.GaussianBlur(roi, (kx, ky), 0)

def apply_pixelate(roi, block_size=PIXELATE_BLOCK_SIZE):
    (h, w) = roi.shape[:2]
    x = max(1, w // block_size)
    y = max(1, h // block_size)
    temp = cv2.resize(roi, (x,y), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

def detect_faces(gray, scale=SCALE_FACTOR):
    faces = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=scale, 
        minNeighbors=5, 
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
        )
    return faces

def main():
    global BLUR_TYPE, SHOW_DETECTION_RECT

    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise RuntimeError(f'Failed to open camera with index {CAM_INDEX}')
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
#    time.sleep(2.0)  # Allow camera to warm up
    last_time = time.time()
    fps = 0
    frame_count = 0
    t0=time.time()
    paused = 0
    print('Starting video stream. Press q to quit. s to toggle blur type. f to toggle rects. p to pause.')
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print('Failed to read frame from camera. Exiting.')
                break
            original = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray)

            for (x, y, w, h) in faces:
                x, y = max(0, x), max(0, y)
                x2, y2 = min(frame.shape[1], x + w), min(frame.shape[0], y + h)
                roi = frame[y:y2, x:x2]
                if roi.size == 0:
                    continue
                if BLUR_TYPE == 'Gaussian':
                    blurred_roi = apply_blur(roi)
                else:
                    blurred_roi = apply_pixelate(roi)
                frame[y:y2, x:x2] = blurred_roi

                if SHOW_DETECTION_RECT:
                    cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)

            frame_count += 1
            if time.time() - t0 >= 1.0:
                fps = frame_count / (time.time() - t0)
                t0 = time.time()
                frame_count = 0

            cv2.putText(frame, f'Blur: {BLUR_TYPE} | FPS: {fps:.1f}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.imshow('Face Blur (press q to quit)', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            BLUR_TYPE = 'pixelate' if BLUR_TYPE == 'gaussian' else 'gaussian'
            print('Toggled blur to', BLUR_TYPE)
        elif key == ord('f'):
            SHOW_DETECTION_RECT = not SHOW_DETECTION_RECT
            print('Show detection rect:', SHOW_DETECTION_RECT)
        elif key == ord('p'):
            paused = not paused
            print('Paused' if paused else 'Resumed')

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
