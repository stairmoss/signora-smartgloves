Smart Gloves Project: Gesture-to-Speech Converter
This project enables smart gloves equipped with flex sensors to interpret hand gestures and convert them into spoken phrases using a Python script. The system consists of an Arduino Nano that reads flex sensor data and sends it to a PC, where a Python application processes the data and uses text-to-speech to vocalize predefined phrases.

Table of Contents
Project Overview

Features

Hardware Requirements

Software Requirements

Setup Instructions

Arduino Setup

Python Setup

Usage

Customization

Troubleshooting

Credits

1. Project Overview
The Smart Gloves project aims to provide a communication aid by translating specific hand gestures into spoken words or phrases. This is achieved by:

Arduino Nano: Reading analog values from flex sensors attached to each finger.

Serial Communication: Sending these flex sensor values to a connected PC via USB.

Python Application: Receiving the serial data, interpreting finger bends based on predefined thresholds, mapping finger states to specific gestures, and then using a text-to-speech engine to vocalize the corresponding phrase.

2. Features
Real-time gesture recognition.

Text-to-speech output for predefined phrases.

Customizable gestures and phrases.

Easy-to-understand Python and Arduino code.

3. Hardware Requirements
Arduino Nano: 1 unit (or compatible Arduino board)

Flex Sensors: 5 units (one for each finger: Thumb, Index, Middle, Ring, Pinky)

Resistors: 5 units (appropriate for your flex sensors, typically 10k Ohm, for voltage dividers)

Breadboard and Jumper Wires: For prototyping

USB Cable: For connecting Arduino Nano to PC

Gloves: To mount the flex sensors (e.g., a simple fabric glove)

4. Software Requirements
Arduino IDE: For programming the Arduino Nano. Download from arduino.cc.

Python 3: Installed on your PC. Download from python.org.

Python Libraries:

pyserial: For serial communication with Arduino.

pyttsx3: For text-to-speech functionality.

5. Setup Instructions
Arduino Setup
Wiring:

Connect each flex sensor to an analog input pin on the Arduino (e.g., A0, A1, A2, A3, A4).

For each flex sensor, create a voltage divider circuit. A common setup involves connecting one end of the flex sensor to 5V, the other end to an analog input pin, and then connecting a pull-down resistor (e.g., 10k Ohm) from that same analog input pin to GND. Refer to your flex sensor's datasheet for the recommended wiring.

Arduino Code:

Open the Arduino IDE.

Copy and paste the following code into a new sketch:

// Arduino Code for Smart Gloves
// Connect flex sensors to Analog Pins A0, A1, A2, A3, A4
// Ensure you have pull-down resistors for your flex sensors as per their datasheet

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
                      // IMPORTANT: This must match the BAUD_RATE in your Python code
}

void loop() {
  // Read analog values from flex sensors
  // Order: Thumb, Index, Middle, Ring, Pinky
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

Select Board and Port: Go to Tools > Board > Arduino Nano (or your specific board). Then, go to Tools > Port and select the serial port your Arduino Nano is connected to.

Upload: Click the "Upload" button (right arrow icon) to compile and upload the code to your Arduino Nano.

Important: After uploading, close the Arduino IDE's Serial Monitor if it's open. The Python script needs exclusive access to the serial port.

Python Setup
Install Python Libraries:

Open your terminal or command prompt.

Run the following commands to install the necessary libraries:

pip install pyserial pyttsx3

For Text-to-Speech (pyttsx3):

Linux users: You might need to install espeak if you don't have a default TTS engine. For example, on Debian/Ubuntu: sudo apt-get install espeak.

Save the Python Code:

Save the provided Python code (from the smart-gloves-python-code immersive) as a .py file (e.g., smart_gloves_control.py).

Configure Serial Port:

Open your saved Python file in a text editor.

Identify the SERIAL_PORT variable:

SERIAL_PORT = 'COM4' # This is the example value from the immersive

Find your Arduino's COM Port:

Connect your Arduino Nano to your PC.

In the Arduino IDE, go to Tools > Port and note down the port name (e.g., COM4 on Windows, /dev/ttyUSB0 or /dev/ttyACM0 on Linux, /dev/cu.usbmodemXXXX on macOS).

Update the SERIAL_PORT variable in your Python code with the correct port for your system.

Adjust FLEX_THRESHOLD (Optional but Recommended):

The FLEX_THRESHOLD = 90 value determines when a finger is considered "bent" or "straight."

You might need to calibrate this. Run the Python script and observe the Flex Values printed in the console when your fingers are straight and when they are bent. Adjust FLEX_THRESHOLD so that values less than or equal to it mean "bent" and values greater than it mean "straight" for your specific sensors.

6. Usage
Ensure Arduino is Connected: Plug your Arduino Nano (with the flex sensors and code uploaded) into your PC via USB.

Close Arduino Serial Monitor: Make sure the Arduino IDE's Serial Monitor is closed.

Run the Python Script:

Open your terminal or command prompt.

Navigate to the directory where you saved smart_gloves_control.py.

Execute the script:

python smart_gloves_control.py

Perform Gestures:

Once the script starts, it will connect to the Arduino and begin listening for data.

Perform the predefined gestures with your smart gloves. The Python script will detect the finger states and speak the corresponding phrase.

The console will show the raw flex values, the interpreted finger states, and the detected gesture.

7. Customization
You can easily customize the project by modifying the GESTURES dictionary in the Python code:

GESTURES = {
    (1, 1, 1, 1, 1): "we are innovator from vvp", # All fingers straight
    (0, 1, 1, 1, 1): "my name is adarsh , his name is Thejus.R , and his name is Karthik .TS", # Thumb bent
    # ... existing gestures ...
    (0, 0, 0, 1, 1): "I need help", # Example: Three fingers bent
    (1, 1, 0, 0, 0): "Good morning", # Example: Three fingers bent
    # Add new gestures here:
    (0, 1, 0, 1, 0): "How are you?", # Example: Index and Ring straight, others bent
    (1, 0, 0, 0, 0): "Yes", # Example: Only thumb straight
}

Key Format: The keys are tuples representing the state of (Thumb, Index, Middle, Ring, Pinky).

0 means the finger is bent (flex sensor value is <= FLEX_THRESHOLD).

1 means the finger is straight (flex sensor value is > FLEX_THRESHOLD).

Value Format: The values are the strings that will be spoken when that specific gesture is detected.

8. Troubleshooting
serial.SerialException: Could not open serial port 'COMX':

Incorrect COM Port: Double-check that SERIAL_PORT in your Python code matches the port your Arduino is using.

Serial Monitor Open: Ensure the Arduino IDE's Serial Monitor is closed. Only one program can access the port at a time.

Arduino Not Connected/Driver Issues: Make sure your Arduino is properly connected and its drivers are installed.

No Speech Output / pyttsx3 Errors:

Library Not Installed: Ensure pyttsx3 is installed (pip install pyttsx3).

TTS Engine Missing (Linux): On Linux, you might need to install espeak or another TTS engine.

Volume/Mute: Check your system's volume and ensure it's not muted.

Incorrect Gesture Detection:

FLEX_THRESHOLD Calibration: Adjust the FLEX_THRESHOLD value in the Python code. Observe the raw flex sensor values in the console when fingers are bent and straight to find an appropriate threshold.

Sensor Wiring/Placement: Ensure your flex sensors are correctly wired and securely attached to the gloves in a way that accurately reflects finger movement.

Gesture Definitions: Review and adjust the GESTURES dictionary mappings to match the actual finger states produced by your gestures.

"Received unexpected number of values" Warning:

This means the Python script received a line from Arduino that didn't contain exactly 5 comma-separated values.

Check your Arduino code to ensure it's always sending 5 values and a newline character (Serial.println(pinkyFlex);).

Check for loose connections or noise on the serial line.

9. Credits
Innovators from VVP: Adarsh, Thejus.R, Karthik.TS

Project Name: Signora


Special Thanks: To the judges for their time and consideration.
