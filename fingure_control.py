import cv2
import mediapipe as mp
import serial
import time

# Initialize serial connection to Arduino
arduino = serial.Serial('COM5', 9600)  # Change 'COM3' to your port (e.g., '/dev/ttyUSB0' for Linux)
time.sleep(2)  # Allow time for connection

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    """
    Function to count raised fingers.
    Thumb logic: Compare tip and MCP x-coordinates
    Other fingers: Compare tip and PIP y-coordinates
    """
    finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    finger_pip = [2, 6, 10, 14, 18]  # PIP joints for fingers

    fingers = []
    
    # Check thumb (x-axis comparison for left hand, right-hand reversed)
    if hand_landmarks.landmark[finger_tips[0]].x > hand_landmarks.landmark[finger_pip[0]].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Check other fingers (y-axis comparison)
    for tip, pip in zip(finger_tips[1:], finger_pip[1:]):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)  # Return total number of fingers raised

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for a mirror effect
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks)
            
            # Send finger count to Arduino
            arduino.write(str(finger_count).encode())

            # Display finger count on the screen
            cv2.putText(frame, f"Fingers: {finger_count}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Finger Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
