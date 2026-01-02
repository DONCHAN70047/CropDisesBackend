import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import numpy as np

def train_model(X_train, y_train, X_val=None, y_val=None, save_path="ml_model.h5"):
    """
    Train a simple CNN model on image data
    """
    num_classes = len(np.unique(y_train))
    input_shape = X_train.shape[1:]  # (224,224,3)

    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val) if X_val is not None else None,
        epochs=5,
        batch_size=8
    )

    model.save(save_path)
    print(f"Model saved to {save_path}")
    return model
