import numpy as np
import os, json
import tensorflow as tf
from model import build_model


CONFIG = json.load(open('training/config.json'))
LABELS = open('training/labels.txt').read().splitlines()


DATASET = "dataset_mfcc/"


X, Y = [], []


for idx, label in enumerate(LABELS):
    folder = os.path.join(DATASET, label)
    for f in os.listdir(folder):
        if f.endswith('.npy'):
            mfcc = np.load(os.path.join(folder, f))
            X.append(mfcc)
            Y.append(idx)


X = np.array(X)
Y = np.array(Y)

# Asegurar shapes consistentes
print("Shapes únicos:", {x.shape for x in X})

# Agregar canal
X = X[..., np.newaxis]

# MEZCLAR ANTES DEL SPLIT
indices = np.arange(len(X))
np.random.shuffle(indices)

X = X[indices]
Y = Y[indices]


model = build_model(len(LABELS))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


model.fit(X, Y, epochs=CONFIG['epochs'], batch_size=CONFIG['batch_size'], validation_split=0.2)


model.export('models/saved_model')

converter = tf.lite.TFLiteConverter.from_saved_model('models/saved_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()


open('models/kws_model.tflite','wb').write(tflite_model)


# Convert to .h
import binascii

with open("models/kws_model.tflite", "rb") as f:
    data = f.read()

hex_array = binascii.hexlify(data).decode("utf-8")
hex_list = [f"0x{hex_array[i:i+2]}" for i in range(0, len(hex_array), 2)]

with open("models/kws_model.h", "w") as f:
    f.write("const unsigned char kws_model[] = {\n")
    for i in range(0, len(hex_list), 12):
        f.write("  " + ", ".join(hex_list[i:i+12]) + ",\n")
    f.write("};\n")
    f.write(f"const unsigned int kws_model_len = {len(data)};\n")