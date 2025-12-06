import os
import numpy as np
import librosa
import json


PARAMS = json.load(open('preprocessing/mfcc_params.json'))

SAMPLE_RATE = PARAMS['sample_rate']
NUM_MEL = PARAMS['num_mel_bins']
NUM_COEFFS = PARAMS['num_coeffs']

DATASET = "C:/Users/Ari/Desktop/keyword-spotting/data/"
OUT = "C:/Users/Ari/Desktop/keyword-spotting/dataset_mfcc/"

os.makedirs(OUT, exist_ok=True)

for label in os.listdir(DATASET):
    indir = os.path.join(DATASET, label)
    if not os.path.isdir(indir):
        continue

    outdir = os.path.join(OUT, label)
    os.makedirs(outdir, exist_ok=True)

    for fname in os.listdir(indir):
        if not fname.endswith('.wav'):
            continue

        path = os.path.join(indir, fname)

        # Load audio
        audio, sr = librosa.load(path, sr=SAMPLE_RATE)

        # Ensure fixed-length audio (1 sec)
        if len(audio) < SAMPLE_RATE:
            audio = np.pad(audio, (0, SAMPLE_RATE - len(audio)))
        else:
            audio = audio[:SAMPLE_RATE]

        # Extract MFCC
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=SAMPLE_RATE,
            n_mfcc=NUM_COEFFS,
            n_mels=NUM_MEL,
            hop_length=320,
            n_fft=640
        )

        mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)

        # Save as .npy
        np.save(os.path.join(outdir, fname.replace(".wav", ".npy")), mfcc)



print("MFCC dataset generated.")