- ESP32 32, 33, visuales
- ESP23 23, 22, maestro
Pin 25 Audio
pin 34 pulsador

Conexiones: Serial
GPIO 23 (TX),→,GPIO 32 (RX)
GPIO 22 (RX),←,GPIO 33 (TX)
GND,↔,GND

| Pantalla ST7789 | Función         | ESP32             |
| --------------- | --------------- | ----------------- |
| **GND**         | Tierra          | GND               |
| **VCC**         | +3.3V           | 3.3V              |
| **SCL**         | SPI Clock (SCK) | **GPIO 18**       |
| **SDA**         | SPI Data (MOSI) | **GPIO 19**       |
| **RES**         | Reset           | **GPIO 5**        |
| **DC**          | Data/Command    | **GPIO 21**       |
| **BLK**         | Backlight       | 3.3V o un pin PWM |
