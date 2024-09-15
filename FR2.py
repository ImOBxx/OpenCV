import cv2

# Load the trained XML classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Capture frames from a camera
cap = cv2.VideoCapture(0)

# Dummy data for name, age, and gender
name = "OB"
age = 25  # Example age
gender = "Male"  # Example gender

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces of different sizes in the input image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces and add the information
    for (x, y, w, h) in faces:
        # Draw the rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Calculate positions for the text
        text_x = x
        text_y = y + h + 25  # Position for the name
        
        # Display the name
        cv2.putText(frame, f"Name: {name}", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Display the age below the name
        cv2.putText(frame, f"Age: {age}", (text_x, text_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Display the gender below the age
        cv2.putText(frame, f"Gender: {gender}", (text_x, text_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Display the output frame
    cv2.imshow('img', frame)

    # Wait for a key press
    if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
