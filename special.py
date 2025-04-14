import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Function to count raised fingers
def count_fingers(hand_landmarks):
    # Hand landmarks indices for fingers (4 -> Thumb, 8 -> Index, 12 -> Middle, 16 -> Ring, 20 -> Pinky)
    finger_tips = [4, 8, 12, 16, 20]
    count = 0

    # Compare each finger tip to its corresponding lower landmark to check if it is raised
    for i, tip in enumerate(finger_tips[1:]):  # Skip thumb for simplicity
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:  # Check if finger is raised
            count += 1

    # Check thumb separately (based on x position for right hand)
    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_tips[0] - 1].x:
        count += 1

    return count

# Initialize drawing variables
drawing = False  # Drawing mode (true if drawing)
draw_color = (0, 0, 255)  # Drawing color (red)
thickness = 5  # Line thickness
canvas = None  # Canvas to draw on

# Start capturing video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the frame horizontally for easier drawing experience
    frame = cv2.flip(frame, 1)

    # Create a whiteboard (black canvas) to draw on
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert the frame to RGB as Mediapipe expects RGB images
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on the hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Count raised fingers for the hand
            fingers_up = count_fingers(hand_landmarks)

            # Check if exactly 1 finger (index finger) is raised for drawing
            if fingers_up == 1:
                index_finger_tip = hand_landmarks.landmark[8]  # Index finger tip
                h, w, _ = frame.shape
                x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                if drawing:  # If already drawing, continue
                    cv2.circle(canvas, (x, y), thickness, draw_color, -1)

                # Draw a circle at the fingertip location
                cv2.circle(frame, (x, y), 10, draw_color, -1)

            # Check if more than 1 finger is raised to stop drawing
            if fingers_up > 1:
                drawing = False
            else:
                drawing = True  # Start drawing when exactly 1 finger is raised

    # Combine the canvas and the frame
    frame = cv2.add(frame, canvas)

    # Display the frame
    cv2.imshow('Hand Detection Whiteboard', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
