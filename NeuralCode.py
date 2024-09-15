import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Create a simple neural network model
model = Sequential()

# Input layer (input_dim should be equal to the number of features in your data)
model.add(Dense(16, input_dim=2, activation='relu'))

# Hidden layer
model.add(Dense(8, activation='relu'))

# Output layer (for binary classification)
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()

# Dummy data for illustration (replace with your dataset)
import numpy as np
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([0, 1, 1, 0])

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=1)

# Evaluate the model
loss, accuracy = model.evaluate(X_train, y_train)
print(f'Loss: {loss}, Accuracy: {accuracy}')
