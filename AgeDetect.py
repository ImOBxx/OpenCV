import cv2
import dlib
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)  # '0' is usually the default ID for the primary webcam

# Load the age detection model
age_weights = "age_net.caffemodel"
age_config = "age_deploy.prototxt"
age_Net = cv2.dnn.readNet(age_config, age_weights)

# Load the gender detection model
gender_weights = "gender_net.caffemodel"
gender_config = "gender_deploy.prototxt"
gender_Net = cv2.dnn.readNet(gender_config, gender_weights)

# Model parameters
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']
model_mean = (78.4263377603, 87.7689143744, 114.895847746)

# Initialize the face detector
face_detector = dlib.get_frontal_face_detector()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to capture image from webcam.")
        break

    # Convert to grayscale for face detection
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(img_gray)

    # If no faces are detected
    if not faces:
        cv2.putText(frame, 'No face detected', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        for face in faces:
            x, y, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 200, 200), 2)

            # Extract and preprocess the face
            face_img = frame[y:y2, x:x2]
            blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), model_mean, swapRB=False)

            # Predict the gender
            gender_Net.setInput(blob)
            gender_preds = gender_Net.forward()
            gender = genderList[gender_preds[0].argmax()]

            # Predict the age
            age_Net.setInput(blob)
            age_preds = age_Net.forward()
            age = ageList[age_preds[0].argmax()]

            # Display the age and gender on the frame
            label = f"{gender}, {age}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow("Age and Gender Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
