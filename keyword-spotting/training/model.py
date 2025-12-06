import tensorflow as tf
from tensorflow.keras import layers, models


def build_model(num_labels):
    return models.Sequential([
    layers.Input(shape=(51, 10, 1)),
    layers.Conv2D(8, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(16, (3,3), activation='relu'),
    layers.Flatten(),
    layers.Dense(32, activation='relu'),
    layers.Dense(num_labels, activation='softmax')
    ])