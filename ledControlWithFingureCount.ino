int ledPins[] = {3, 4, 5}; // Pins for LEDs
int numLeds = 53;
char receivedData; // Variable to store received data

void setup() {
    Serial.begin(9600); // Start serial communication
    for (int i = 0; i < numLeds; i++) {
        pinMode(ledPins[i], OUTPUT);
    }
}

void loop() {
    if (Serial.available() > 0) {
        receivedData = Serial.read();
        int fingerCount = receivedData - '0'; // Convert char to int

        for (int i = 0; i < numLeds; i++) {
            if (i < fingerCount) {
                digitalWrite(ledPins[i], HIGH);
            } else {
                digitalWrite(ledPins[i], LOW);
            }
        }
    }
}
