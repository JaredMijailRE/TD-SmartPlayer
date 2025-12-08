#include "AudioTools.h"
#include "BluetoothA2DPSink.h"
#include <Arduino.h>

AnalogAudioStream out;
BluetoothA2DPSink a2dp_sink(out);

// Pin definitions
const int BUTTON_PIN = 32;      // Changed to 32 (supports internal pull-up)
const int LED_PIN = 2;          // Built-in LED
const float VOLUME_BOOST = 4.0; // Multiplicador de volumen
// Internal DAC outputs automatically on GPIO 25 (Channel 1) and GPIO 26
// (Channel 2)

// State variables
volatile bool is_connected = false;

// Button logic
bool isButtonPressed() {
  return digitalRead(BUTTON_PIN) == LOW;
} // Active LOW with pull-up

// Callback when connection state changes
void connection_state_changed(esp_a2d_connection_state_t state, void *) {
  if (state == ESP_A2D_CONNECTION_STATE_CONNECTED) {
    is_connected = true;
    digitalWrite(LED_PIN, HIGH); // LED encendido cuando está conectado
    Serial.println("Dispositivo conectado!");
  } else {
    is_connected = false;
    Serial.println("Dispositivo desconectado - buscando...");
  }
}

// Callback para amplificar el audio manualmente
void read_data_stream(const uint8_t *data, uint32_t length) {
  int16_t *samples = (int16_t *)data;
  uint32_t sample_count = length / 2;

  // Amplificar cada muestra
  for (uint32_t i = 0; i < sample_count; i++) {
    int32_t amplified = samples[i] * VOLUME_BOOST;

    // Aplicar clipping para evitar distorsión extrema
    if (amplified > 32767)
      amplified = 32767;
    if (amplified < -32768)
      amplified = -32768;

    samples[i] = (int16_t)amplified;
  }

  // Escribir al DAC
  out.write(data, length);
}

void setup() {
  Serial.begin(115200);
  Serial.println("Iniciando ESP32 Bluetooth Speaker...");

  pinMode(BUTTON_PIN, INPUT_PULLUP); // Enable internal pull-up resistor
  pinMode(LED_PIN, OUTPUT);          // Configure LED pin
  digitalWrite(LED_PIN, LOW);        // Start with LED off (searching)

  // Configure AnalogAudioStream
  auto cfg = out.defaultConfig(TX_MODE);
  cfg.sample_rate = 44100;
  cfg.channels = 2;
  cfg.bits_per_sample = 16;
  cfg.buffer_size = 512;
  cfg.buffer_count = 8;

  out.begin(cfg);

  // Configurar callback de amplificación
  a2dp_sink.set_stream_reader(read_data_stream, false);

  // Register connection state callback
  a2dp_sink.set_on_connection_state_changed(connection_state_changed);

  // Start the Bluetooth A2DP sink
  a2dp_sink.start("ESP32-Music");

  Serial.println("Bluetooth iniciado: ESP32-Music");
  Serial.print("Volumen configurado al: ");
  Serial.print(VOLUME_BOOST * 100);
  Serial.println("%");
  Serial.println("Conecta tu telefono y reproduce musica.");
  Serial.println("Presiona el boton en Pin 32 para desconectar/buscar.");
}

void loop() {
  // LED blinking when not connected (pairing mode)
  if (!is_connected) {
    static unsigned long lastBlink = 0;
    static bool ledState = false;

    if (millis() - lastBlink > 500) { // Blink every 500ms
      lastBlink = millis();
      ledState = !ledState;
      digitalWrite(LED_PIN, ledState ? HIGH : LOW);
    }
  }

  // Button logic to disconnect/search
  if (isButtonPressed()) {
    delay(50); // Debounce
    if (isButtonPressed()) {
      Serial.println("Boton presionado...");
      unsigned long pressTime = millis();
      bool actionTaken = false;

      while (isButtonPressed()) {
        if (millis() - pressTime > 1000 && !actionTaken) {
          Serial.println("Boton mantenido: Desconectando para buscar nuevos "
                         "dispositivos...");
          a2dp_sink.disconnect();
          actionTaken = true;
        }
        delay(10);
      }
    }
  }
  delay(100);
}
