// Arduino Code for Smart Gloves (Upload this to your Arduino Nano)
// Connect flex sensors to Analog Pins A0, A1, A2, A3, A4
// (Ensure you have pull-down or pull-up resistors for your flex sensors as per their datasheet)

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
                    // IMPORTANT: This must match the BAUD_RATE in your Python code
}

void loop() {
  // Read analog values from flex sensors
  // Adjust pin assignments based on your wiring
  int thumbFlex = analogRead(A0);
  int indexFlex = analogRead(A1);
  int middleFlex = analogRead(A2);
  int ringFlex = analogRead(A3);
  int pinkyFlex = analogRead(A4);

  // Print the values to the serial monitor, separated by commas
  // The Python script will read these values
  Serial.print(thumbFlex);
  Serial.print(",");
  Serial.print(indexFlex);
  Serial.print(",");
  Serial.print(middleFlex);
  Serial.print(",");
  Serial.print(ringFlex);
  Serial.print(",");
  Serial.println(pinkyFlex); // Use println to send a newline character at the end

  delay(100); // Small delay to prevent flooding the serial port
}