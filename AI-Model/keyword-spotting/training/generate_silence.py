import os
import numpy as np
import librosa
import soundfile as sf

INPUT_DIR = "data/_background_noise_"
OUTPUT_DIR = "data/_background_noise_"
SAMPLE_RATE = 16000
CHUNK_DURATION = 1.0   # 1 segundo
CHUNK_SAMPLES = int(SAMPLE_RATE * CHUNK_DURATION)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_silences():
    ensure_dir(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".wav")]
    if not files:
        print("❌ No se encontraron archivos .wav en", INPUT_DIR)
        return

    counter = 0

    for file in files:
        filepath = os.path.join(INPUT_DIR, file)
        print("Procesando:", filepath)

        # Cargar audio
        audio, sr = librosa.load(filepath, sr=SAMPLE_RATE)

        # Cortar en segmentos de 1s
        total_samples = len(audio)
        num_chunks = total_samples // CHUNK_SAMPLES

        for i in range(num_chunks):
            start = i * CHUNK_SAMPLES
            end = start + CHUNK_SAMPLES
            chunk = audio[start:end]

            out_path = os.path.join(OUTPUT_DIR, f"generated_{counter}.wav")
            sf.write(out_path, chunk, SAMPLE_RATE)
            counter += 1

    print(f"✔ Generadas {counter} muestras nuevas de silencio")

if __name__ == "__main__":
    generate_silences()