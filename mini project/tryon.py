import cv2
import numpy as np

# Load the Haar Cascade for full body detection
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Load the dress images with transparency (ensure they are PNG with alpha channel)
dress_images = {
    "State1": cv2.imread("dress1.png", cv2.IMREAD_UNCHANGED),  # Replace with your dress image paths
    "State2": cv2.imread("dress2.png", cv2.IMREAD_UNCHANGED),
}

def overlay_dress(frame, x, y, width, height, dress_img):
    # Resize the dress to match the detected body dimensions
    dress_resized = cv2.resize(dress_img, (width, height))
    
    # Separate the color channels and alpha channel
    dress_bgr = dress_resized[:, :, :3]  # BGR channels
    dress_alpha = dress_resized[:, :, 3]  # Alpha channel
    
    # Create masks
    _, mask = cv2.threshold(dress_alpha, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    # Define region of interest (ROI)
    roi = frame[y:y+height, x:x+width]
    
    # Ensure ROI is within the frame boundaries
    if roi.shape[:2] != (height, width):
        return
    
    # Apply masks to the ROI and dress
    frame_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    dress_fg = cv2.bitwise_and(dress_bgr, dress_bgr, mask=mask)
    
    # Combine the background and the dress
    dst = cv2.add(frame_bg, dress_fg)
    frame[y:y+height, x:x+width] = dst

def run_virtual_dressing_room():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break
        
        # Convert frame to grayscale for body detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect bodies in the frame
        bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        for (x, y, w, h) in bodies:
            # Select a dress image (example uses "State1")
            selected_dress = dress_images["State1"]
            if selected_dress is not None:
                overlay_dress(frame, x, y, w, h, selected_dress)
            else:
                print("Error: Dress image not loaded.")
        
        # Display the frame
        cv2.imshow('Virtual Dressing Room', frame)
        
        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Run the virtual dressing room application
run_virtual_dressing_room()
