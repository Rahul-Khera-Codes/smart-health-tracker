import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
import os

# Set random seed for reproducibility
tf.random.set_seed(42)

# Load health data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Preprocess data
def preprocess_data(data):
    try:
        # Assuming the last column is the target variable
        X = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values
        # Normalize features
        X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
        return X, y
    except Exception as e:
        print(f"Error preprocessing data: {e}")
        return None, None

# Build the model
def build_model(input_shape):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(input_shape,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # Assuming binary classification
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train the model
def train_model(model, X_train, y_train, epochs=50, batch_size=32):
    try:
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)
    except Exception as e:
        print(f"Error during model training: {e}")

# Save the model
def save_model(model, model_path):
    try:
        model.save(model_path)
    except Exception as e:
        print(f"Error saving model: {e}")

if __name__ == "__main__":
    data_file_path = 'data/health_data.csv'  # Update with actual data file path
    model_save_path = 'models/health_insights_model.h5'

    data = load_data(data_file_path)
    if data is not None:
        X, y = preprocess_data(data)
        if X is not None and y is not None:
            model = build_model(X.shape[1])
            train_model(model, X, y)
            save_model(model, model_save_path)