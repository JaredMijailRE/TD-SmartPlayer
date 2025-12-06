import os
import random
import shutil
import glob

BASE = "C:/Users/Ari/Desktop/keyword-spotting/data/"

CLASSES = [
    "stop",
    "go",
    "up",
    "down",
    "left",
    "right",
    "_background_noise_"
]

# Crear carpetas de splits
for split in ["train", "val", "test"]:
    for c in CLASSES:
        os.makedirs(os.path.join(BASE, split, c), exist_ok=True)

# Cargar archivos
all_files = {}
for c in CLASSES:
    folder = os.path.join(BASE, c)
    all_files[c] = glob.glob(os.path.join(folder, "*.wav"))

def split_list(lst):
    random.shuffle(lst)
    n = len(lst)
    return lst[:int(n*0.8)], lst[int(n*0.8):int(n*0.9)], lst[int(n*0.9):]

# Generar splits
for c in CLASSES:
    train, val, test = split_list(all_files[c])

    for src, split in [(train, "train"), (val, "val"), (test, "test")]:
        for f in src:
            shutil.copy(
                f,
                os.path.join(BASE, split, c, os.path.basename(f))
            )

print("Splits creados sin UNKNOWN ni SILENCE.")