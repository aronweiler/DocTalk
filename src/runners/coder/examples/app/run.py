import cv2
from cv2 import CascadeClassifier

# Initialize the webcam and check if it is available
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    logging.debug("No webcam found.")
    exit()

# Connect to the webcam and start streaming the video feed
while True:
    # Read a frame from the webcam
    ret, frame = webcam.read()
    
    # Check if the frame was successfully read
    if not ret:
        logging.debug("Failed to read frame from webcam.")
        break
    
    # Perform face detection on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Draw a box around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display the frame with the detected faces
    cv2.imshow('Face Detection', frame)
    
    # Check for key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close any open windows
webcam.release()
cv2.destroyAllWindows()