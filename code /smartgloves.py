import serial
import pyttsx3
import time
import collections
import threading
import logging

# --- Configuration ---
COM_PORT = 'COM6'  # Update to your actual COM port
BAUD_RATE = 9600
BENT_THRESHOLD = 90
STRAIGHT_THRESHOLD = 90
MIN_FLEX_VALUE = 10

MIN_SPEAK_INTERVAL = 1.5  # Reduced for faster response
GESTURE_HOLD_TIME = 0.8

last_spoken_time = 0
current_held_gesture = None
gesture_start_time = 0

speech_queue = collections.deque()
speaking_thread = None
speech_lock = threading.Lock()
tts_engine = None

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Initialize TTS Engine ---
def init_tts_engine():
    global tts_engine
    try:
        tts_engine = pyttsx3.init('sapi5')
        tts_engine.setProperty('rate', 150)
        tts_engine.setProperty('volume', 0.9)
        
        voices = tts_engine.getProperty('voices')
        if voices:
            tts_engine.setProperty('voice', voices[0].id)
        
        logging.info("TTS engine initialized successfully.")
        return True
    except Exception as e:
        logging.error(f"TTS initialization failed: {e}")
        return False

# --- Speaking Thread ---
def _speak_worker():
    global last_spoken_time, tts_engine
    
    # Initialize TTS engine in this thread
    if not init_tts_engine():
        logging.critical("Failed to initialize TTS engine in worker thread")
        return
    
    while True:
        text_to_speak = None
        
        # Thread-safe queue access
        with speech_lock:
            if speech_queue:
                text_to_speak = speech_queue.popleft()
        
        if text_to_speak:
            current_time = time.time()

            if (current_time - last_spoken_time) > MIN_SPEAK_INTERVAL:
                try:
                    logging.info(f"Speaking: '{text_to_speak}'")
                    
                    # Ensure engine is ready
                    if tts_engine is None:
                        init_tts_engine()
                    
                    if tts_engine:
                        # Stop any ongoing speech
                        tts_engine.stop()
                        
                        # Speak the text
                        tts_engine.say(text_to_speak)
                        tts_engine.runAndWait()
                        
                        last_spoken_time = current_time
                        logging.info(f"Successfully spoke: '{text_to_speak}'")
                    
                except Exception as e:
                    logging.error(f"TTS Error: {e}")
                    # Try to reinitialize engine
                    init_tts_engine()
            else:
                logging.debug(f"Skipping '{text_to_speak}' due to cooldown.")
        
        time.sleep(0.05)  # Shorter sleep for more responsive processing

def speak(text):
    """Add text to speech queue"""
    if text:  # Only add non-empty text
        with speech_lock:
            speech_queue.append(text)
        logging.debug(f"Added to speech queue: '{text}'")

# --- Finger Interpretation ---
def get_finger_state(value):
    if MIN_FLEX_VALUE <= value < BENT_THRESHOLD:
        return 'bent'
    elif value >= STRAIGHT_THRESHOLD:
        return 'straight'
    else:
        return 'indeterminate'

# --- Gesture Definitions ---
GESTURES = {
    ('s', 'b', 'b', 'b', 'b'): "My name is Adarsh, his name is Thejus R, and his name is Karthik TS",
    ('b', 's', 'b', 'b', 'b'): "This project is Signora",
    ('s', 's', 's', 's', 'b'): "This",
    ('b', 'b', 'b', 'b', 's'): "Bring me water",
    ('s', 'b', 's', 'b', 'b'): "Bring me medicines",
    ('b', 'b', 's', 'b', 'b'): "Need to go to toilet",
    ('b', 'b', 'b', 's', 'b'): "Thank you",
    ('s', 's', 'b', 'b', 'b'): "Welcome",
    ('b', 'b', 'b', 'b', 'b'): "Hello judges",
    ('s', 's', 'b', 's', 's'): "VVP",
    ('s', 'b', 'b', 'b', 's'): "Are",
    ('b', 's', 'b', 's', 'b'): "Patients",
    ('s', 's', 'b', 'b', 's'): "Yes",
    ('b', 's', 's', 'b', 'b'): "No",
    ('b', 'b', 's', 's', 'b'): "Help",
    ('s', 'b', 'b', 's', 'b'): "Food",
}

last_spoken_gesture = None

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting Smart Gloves System...")
    
    # Start speaking thread
    speaking_thread = threading.Thread(target=_speak_worker, daemon=True)
    speaking_thread.start()
    
    # Give the TTS thread time to initialize
    time.sleep(2)
    
    # Test the TTS system
    speak("Smart gloves system activated")
    print("TTS test message sent.")
    
    # Wait for initial message to complete
    time.sleep(3)

    ser = None
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to Arduino on {COM_PORT} at {BAUD_RATE} baud.")
        
        # Clear any initial data
        ser.flushInput()
        
        print("System ready! Make gestures...")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()

                try:
                    values_str = line.split(',')
                    finger_values = [int(v) for v in values_str]

                    if len(finger_values) == 5:
                        current_finger_states = tuple(get_finger_state(val) for val in finger_values)

                        simplified_states = tuple(
                            's' if s == 'straight' else 'b' if s == 'bent' else 'x'
                            for s in current_finger_states
                        )

                        print(f"Finger states: {simplified_states}")  # Debug output

                        # Reset if indeterminate values
                        if 'x' in simplified_states:
                            current_held_gesture = None
                            gesture_start_time = 0
                            continue

                        # Reset if all fingers straight
                        all_fingers_straight = all(s == 's' for s in simplified_states)
                        if all_fingers_straight:
                            current_held_gesture = None
                            gesture_start_time = 0
                            continue

                        # Check for gesture match
                        potential_gesture_pattern = None
                        potential_gesture_phrase = None

                        for pattern, phrase in GESTURES.items():
                            if pattern == simplified_states:
                                potential_gesture_pattern = pattern
                                potential_gesture_phrase = phrase
                                break

                        if potential_gesture_pattern:
                            # New gesture detected
                            if current_held_gesture != potential_gesture_pattern:
                                current_held_gesture = potential_gesture_pattern
                                gesture_start_time = time.time()
                                print(f"New gesture detected: {potential_gesture_phrase}")

                            # Check if gesture held long enough
                            if (time.time() - gesture_start_time) >= GESTURE_HOLD_TIME:
                                if potential_gesture_phrase != last_spoken_gesture:
                                    print(f"🎤 SPEAKING: {potential_gesture_phrase}")
                                    speak(potential_gesture_phrase)  # This will speak the actual word/phrase
                                    last_spoken_gesture = potential_gesture_phrase
                                    current_held_gesture = None
                                    gesture_start_time = 0
                        else:
                            # No gesture match, reset
                            current_held_gesture = None
                            gesture_start_time = 0

                    else:
                        logging.warning(f"Expected 5 values, got {len(finger_values)}: {line}")

                except ValueError:
                    logging.error(f"Invalid number format: '{line}'")
                except Exception as e:
                    logging.error(f"Processing error: {e}")

            time.sleep(0.01)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        print("Make sure Arduino is connected and COM port is correct!")
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed.")
        if tts_engine:
            tts_engine.stop()
        print("Program ending.")
