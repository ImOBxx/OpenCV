import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing import image

# Load the MobileNetV2 model pre-trained on ImageNet
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3), pooling='avg')

# Add a custom head for gender classification
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')  # Two outputs: Male and Female
])

# Verify model prediction with a test input
test_image = np.random.rand(224, 224, 3) * 255
test_image = np.expand_dims(test_image, axis=0)
test_image = preprocess_input(test_image)

try:
    gender_preds = model.predict(test_image)
    print(f"Model test prediction: {gender_preds}")
except Exception as e:
    print(f"Error in model prediction: {e}")

# List of gender labels
gender_list = ['Male', 'Female']

# Load OpenCV's pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture from the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream from webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]

        # Preprocess the face image for MobileNetV2
        face_img = cv2.resize(face, (224, 224))
        x_input = image.img_to_array(face_img)
        x_input = np.expand_dims(x_input, axis=0)
        x_input = preprocess_input(x_input)

        # Predict gender
        try:
            gender_preds = model.predict(x_input)
            gender = gender_list[np.argmax(gender_preds)]
        except Exception as e:
            print(f"Error during gender prediction: {e}")
            gender = "Unknown"

        # Draw the bounding box and the label on the image
        label = f"{gender}"
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the output frame
    cv2.imshow("Gender Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
