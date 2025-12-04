#include "AudioFileSourceLittleFS.h"
#include "AudioGeneratorWAV.h"
#include "AudioOutputI2S.h"
#include "FS.h"
#include "LittleFS.h"
#include <Arduino.h>

AudioGeneratorWAV *wav;
AudioFileSourceLittleFS *file;
AudioOutputI2S *out;

void setup() {
  Serial.begin(115200);
  Serial.println("\n\nESP32 - Audio Playback");

  // Iniciar LittleFS
  if (!LittleFS.begin()) {
    Serial.println("Error al montar LittleFS");
    while (1)
      delay(1000); // Detener si falla
  }

  Serial.println("LittleFS montado correctamente");

  file = new AudioFileSourceLittleFS("/audio.wav");

  // Configurar salida I2S para usar el DAC interno del ESP32
  // 0 = Puerto I2S 0
  // 1 = INTERNAL_DAC (Salida analógica en pines 25 y 26)
  // 8 = DMA buffers
  // 1 = APLL ENABLE (Mejora precision de reloj para 11025Hz)
  out = new AudioOutputI2S(0, 1, 8, 1);

  // Opcional: Ajustar ganancia/volumen
  out->SetGain(2.0);

  wav = new AudioGeneratorWAV();

  if (wav->begin(file, out)) {
    Serial.println("Reproduciendo audio.wav...");
    // Forzar la velocidad de muestreo correcta si la auto-deteccion falla
    out->SetRate(11025);
  } else {
    Serial.println(
        "Error al iniciar reproduccion, revisa si el archivo existe");
  }
}

void loop() {
  if (wav->isRunning()) {
    if (!wav->loop()) {
      wav->stop();
      Serial.println("Fin de reproduccion");
      // Reiniciar para bucle infinito o dejarlo detenido
      // Para reiniciar:
      // file->seek(0, SEEK_SET);
      // wav->begin(file, out);
    }
  } else {
    delay(1000);
  }
}
