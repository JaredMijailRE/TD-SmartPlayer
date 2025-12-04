# Proyecto 4 - PlatformIO

Proyecto de PlatformIO con ESP32 DOIT DevKit V1

## Descripción
Programa Blink LED que parpadea el LED integrado (GPIO2) del ESP32 cada segundo. Incluye salida serial a 115200 baud.

## Estructura
- `src/` - Código fuente
- `include/` - Headers
- `lib/` - Librerías
- `platformio.ini` - Configuración
- `.pio/` - Archivos de compilación

## Requisitos
- PlatformIO CLI instalado
- ESP32 DOIT DevKit V1 conectado en COM9
- En WSL: `usbipd` instalado en Windows

## Comandos

### Compilar el código
```bash
platformio run
```

O con permisos elevados (WSL):
```bash
sudo /home/turing/docs/proyecto4/.venv/bin/platformio run
```

### Subir a la placa ESP32
```bash
platformio run --target upload
```

O con permisos elevados (WSL):
```bash
sudo /home/turing/docs/proyecto4/.venv/bin/platformio run --target upload
```

### Subir archivos al sistema de archivos (LittleFS)
Para subir el archivo `audio.wav` a la placa:
```bash
platformio run --target uploadfs
```

O con permisos elevados (WSL):
```bash
sudo /home/turing/docs/proyecto4/.venv/bin/platformio run --target uploadfs
```

### Monitorear puerto serial
```bash
platformio device monitor --port /dev/ttyUSB0 --baud 115200
```

O con permisos elevados (WSL):
```bash
sudo /home/turing/docs/proyecto4/.venv/bin/platformio device monitor --port /dev/ttyUSB0 --baud 115200
```

### Limpiar archivos compilados
```bash
platformio run --target clean
```

## Configuración WSL
En WSL2 con Windows, ejecuta primero en PowerShell (como administrador):
```powershell
usbipd attach --wsl --busid 1-6
```

Esto conecta el ESP32 a WSL antes de compilar y subir.

