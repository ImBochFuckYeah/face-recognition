# Reconocimiento Facial con Python y Control de LEDs con Arduino

Este proyecto combina el reconocimiento facial utilizando Python con el control de LEDs mediante un Arduino. Cuando el sistema detecta un rostro conocido, enciende un LED verde en el Arduino. Si no reconoce el rostro, enciende un LED rojo.

## Requisitos

### Software
- Python 3.6 o superior
- OpenCV
- face_recognition
- Tkinter
- pyserial
- Arduino IDE

### Hardware
- Arduino (UNO, Mega, etc.)
- LED verde
- LED rojo
- Resistencias (220 ohmios)
- Cables de conexión

## Instalación

### 1. Configurar el Entorno Python

1. Clona este repositorio:
    ```sh
    git clone https://github.com/tu_usuario/reconocimiento-facial-arduino.git
    cd reconocimiento-facial-arduino
    ```

2. Instala las dependencias de Python:
    ```sh
    pip install opencv-python face_recognition pyserial
    ```

### 2. Configurar el Arduino

1. Abre el archivo `arduino_code.ino` en el Arduino IDE.
2. Conecta tu Arduino a la computadora.
3. Selecciona la placa y el puerto correcto en el Arduino IDE.
4. Carga el código en tu Arduino.

## Uso

### 1. Ejecutar el Reconocimiento Facial

Ejecuta el script de Python para iniciar el reconocimiento facial y el control de LEDs:

```sh
python reconocimiento_facial.py
```

### 2. Guardar Nuevos Rostros

- Cuando el sistema detecta un rostro, puedes presionar la tecla `s` para guardar la imagen del rostro capturado.
- Ingresa un nombre para el rostro a través de una ventana emergente.
- El sistema actualizará automáticamente la base de datos de rostros conocidos sin necesidad de reiniciar la aplicación.

### 3. Controles Adicionales

- Presiona `ESC` para cerrar la aplicación.
- Presiona la tecla de `espacio` para simular una interrupción del sistema.

## Funcionamiento

El script de Python realiza el reconocimiento facial utilizando la biblioteca `face_recognition`. Dependiendo de si el rostro es reconocido o no, se envía un carácter ('T' o 'F') al Arduino a través del puerto serial. El Arduino controla dos LEDs basándose en los datos recibidos:

- `T`: Enciende el LED verde (rostro reconocido).
- `F`: Enciende el LED rojo (rostro no reconocido).

## Código del Arduino

```cpp
// Definir los pines para los LEDs
const int greenLedPin = 7; // Pin para el LED verde
const int redLedPin = 8;   // Pin para el LED rojo

void setup() {
  // Inicializar los pines de los LEDs como salidas
  pinMode(greenLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);

  // Inicializar la comunicación serial
  Serial.begin(9600);
}

void loop() {
  // Verificar si hay datos disponibles en el puerto serial
  if (Serial.available() > 0) {
    // Leer el byte recibido
    char receivedChar = Serial.read();

    // Controlar los LEDs basándose en el valor recibido
    if (receivedChar == 'T') {
      digitalWrite(greenLedPin, HIGH); // Encender el LED verde
      digitalWrite(redLedPin, LOW);    // Apagar el LED rojo
    } else if (receivedChar == 'F') {
      digitalWrite(greenLedPin, LOW);  // Apagar el LED verde
      digitalWrite(redLedPin, HIGH);   // Encender el LED rojo
    }
  }
}
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para mejorar este proyecto.

## Licencia

Este proyecto está licenciado bajo la MIT License. Consulta el archivo `LICENSE` para más detalles.