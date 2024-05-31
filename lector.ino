// Definir los pines para los LEDs
const int greenLedPin = 50; // Pin para el LED verde
const int redLedPin = 51;   // Pin para el LED rojo

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