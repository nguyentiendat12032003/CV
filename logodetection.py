import cv2
import numpy as np

def detect_logo(video_path, logo_path, threshold=10):
    # Read logo and convert to HSV
    roi = cv2.imread(logo_path)
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Calculate histogram of logo
    roi_hist = cv2.calcHist([hsv_roi], [0, 1], None, [180, 256], [0, 180, 0, 256])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Set up termination criteria
    term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Calculate back projection
        back_proj = cv2.calcBackProject([hsv_frame], [0, 1], roi_hist, [0, 180, 0, 256], 1)

        # Threshold back projection
        ret, thresh = cv2.threshold(back_proj, threshold, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw rectangle around the logo
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # Adjust area threshold as needed
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display result
        cv2.imshow('Logo Detection (Backprojection)', frame)

        # Exit on 'q' key press
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Paths to video and logo
video_path = "output.mp4"
logo_path = "logo_detection_img.png"

# Call function to detect logo using backprojection
detect_logo(video_path, logo_path)
