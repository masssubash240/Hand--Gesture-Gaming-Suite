import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from collections import deque

# ===== CONFIGURATION =====
GESTURE_COOLDOWN = 0.3  # Seconds between gestures
SHOW_GLOW = True       # Enable subsurface glow effect
GLOW_INTENSITY = 1.5   # Glow strength (1.0-2.0)
CAM_WIDTH = 640
CAM_HEIGHT = 480

# ===== INITIALIZATION =====
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_draw_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

# For gesture cooldown
last_action_time = 0
current_action = None

# FPS calculation
fps_counter = deque(maxlen=30)
prev_time = time.time()

# ===== GESTURE FUNCTIONS =====
def get_finger_states(hand_landmarks):
    """Returns list of finger states [thumb, index, middle, ring, pinky] (1=up, 0=down)"""
    fingers = []
    
    # Thumb (special case - compare x coordinates)
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other 4 fingers
    tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.RING_FINGER_TIP,
            mp_hands.HandLandmark.PINKY_TIP]
    
    dips = [mp_hands.HandLandmark.INDEX_FINGER_DIP,
            mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
            mp_hands.HandLandmark.RING_FINGER_DIP,
            mp_hands.HandLandmark.PINKY_DIP]
    
    for tip, dip in zip(tips, dips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[dip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

def recognize_gesture(fingers):
    """Map finger states to gesture names"""
    if fingers == [0, 0, 0, 0, 0]:
        return "FIST 🤛", "rightclick"  # Aim
    elif fingers == [1, 0, 0, 0, 0]:
        return "THUMBS UP 👍", "leftclick"  # Shoot
    elif fingers == [0, 1, 0, 0, 0]:
        return "INDEX UP ☝️", "w"  # Move Forward
    elif fingers == [0, 1, 1, 0, 0]:
        return "PEACE ✌️", "r"  # Reload
    elif fingers == [1, 1, 1, 1, 1]:
        return "OPEN PALM 🖐️", "space"  # Jump
    elif fingers == [0, 1, 1, 1, 0]:
        return "THREE FINGERS 🤟", "shift"  # Sprint
    else:
        return None, None

def execute_action(action_key):
    """Execute the game control action"""
    global last_action_time, current_action
    
    current_time = time.time()
    
    # Cooldown check
    if current_time - last_action_time < GESTURE_COOLDOWN:
        return current_action
    
    if action_key == "leftclick":
        pyautogui.click()
        print("🔫 SHOOT")
    elif action_key == "rightclick":
        pyautogui.click(button='right')
        print("🎯 AIM")
    elif action_key == "space":
        pyautogui.press('space')
        print("🦘 JUMP")
    elif action_key == "r":
        pyautogui.press('r')
        print("🔄 RELOAD")
    elif action_key == "w":
        pyautogui.keyDown('w')
        print("🏃 MOVE FORWARD")
    elif action_key == "shift":
        pyautogui.keyDown('shift')
        print("💨 SPRINT")
    
    # Release previous keys
    if current_action in ['w', 'shift'] and current_action != action_key:
        pyautogui.keyUp(current_action)
    
    last_action_time = current_time
    current_action = action_key if action_key in ['w', 'shift'] else None
    
    return action_key

# ===== GLOW EFFECT FUNCTION =====
def apply_subsurface_glow(frame):
    """Apply glowing effect to simulate subsurface scattering"""
    if not SHOW_GLOW:
        return frame
    
    # Create blurred layers for glow
    blur1 = cv2.GaussianBlur(frame, (15, 15), 0)
    blur2 = cv2.GaussianBlur(frame, (31, 31), 0)
    blur3 = cv2.GaussianBlur(frame, (61, 61), 0)
    
    # Combine blurs with different intensities
    glow = cv2.addWeighted(blur1, 0.5, blur2, 0.3, 0)
    glow = cv2.addWeighted(glow, 1.0, blur3, 0.2, 0)
    
    # Mix original with glow
    result = cv2.addWeighted(frame, GLOW_INTENSITY, glow, 1 - (GLOW_INTENSITY - 1), 0)
    
    # Enhance colors slightly
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = np.clip(hsv[:,:,1] * 1.1, 0, 255)  # Increase saturation
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return result

# ===== UI OVERLAY =====
def draw_ui(frame, gesture_name, fps):
    """Draw cyberpunk style UI overlay"""
    h, w = frame.shape[:2]
    
    # Create semi-transparent overlay
    overlay = frame.copy()
    
    # Top bar with glow
    cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
    
    # Bottom status bar
    cv2.rectangle(overlay, (0, h-80), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
    
    # Add glowing borders
    cv2.line(frame, (0, 60), (w, 60), (0, 255, 255), 1)
    cv2.line(frame, (0, h-80), (w, h-80), (0, 255, 255), 1)
    
    # FPS Counter with glow effect
    fps_text = f"FPS: {fps:.1f}"
    cv2.putText(frame, fps_text, (w-120, 40), 
                cv2.FONT_HERSHEY_SEMIBOLD, 0.7, (0, 0, 0), 3)
    cv2.putText(frame, fps_text, (w-120, 40), 
                cv2.FONT_HERSHEY_SEMIBOLD, 0.7, (0, 255, 255), 1)
    
    # Current gesture display
    if gesture_name:
        # Outer glow
        cv2.putText(frame, gesture_name, (20, 120), 
                    cv2.FONT_HERSHEY_SEMIBOLD, 1.2, (0, 0, 0), 5)
        cv2.putText(frame, gesture_name, (20, 120), 
                    cv2.FONT_HERSHEY_SEMIBOLD, 1.2, (0, 255, 255), 2)
    
    # Instructions
    instructions = [
        "👍 Shoot | ✊ Aim | ✌️ Reload",
        "🖐️ Jump | ☝️ Forward | 🤟 Sprint"
    ]
    y_offset = h - 40
    for instr in instructions:
        cv2.putText(frame, instr, (20, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
        y_offset += 25
    
    return frame

# ===== MAIN LOOP =====
print("🚀 Hand Gesture Game Controller Started!")
print("🤚 Show your hand to the camera")
print("Press 'q' to quit | 'g' to toggle glow | '+'/'-' to adjust glow")

while True:
    success, frame = cap.read()
    if not success:
        break
    
    # Mirror frame for intuitive control
    frame = cv2.flip(frame, 1)
    
    # Calculate FPS
    curr_time = time.time()
    fps_counter.append(1 / (curr_time - prev_time))
    fps = sum(fps_counter) / len(fps_counter)
    prev_time = curr_time
    
    # Process hand detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    current_gesture = "No Hand Detected"
    
    if results.multi_hand_landmarks:
        # Use first detected hand
        hand_landmarks = results.multi_hand_landmarks[0]
        
        # Draw hand landmarks with custom style
        mp_draw.draw_landmarks(
            frame, 
            hand_landmarks, 
            mp_hands.HAND_CONNECTIONS,
            mp_draw_styles.get_default_hand_landmarks_style(),
            mp_draw_styles.get_default_hand_connections_style()
        )
        
        # Get finger states and recognize gesture
        finger_states = get_finger_states(hand_landmarks)
        gesture_name, action_key = recognize_gesture(finger_states)
        
        if gesture_name and action_key:
            current_gesture = gesture_name
            execute_action(action_key)
    
    # Apply subsurface glow effect
    frame = apply_subsurface_glow(frame)
    
    # Draw UI overlay
    frame = draw_ui(frame, current_gesture, fps)
    
    # Show frame
    cv2.imshow("🎮 Hand Gesture Gaming System - Subsurface Glow", frame)
    
    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('g'):
        SHOW_GLOW = not SHOW_GLOW
        print(f"Glow effect: {'ON' if SHOW_GLOW else 'OFF'}")
    elif key == ord('+') or key == ord('='):
        GLOW_INTENSITY = min(2.0, GLOW_INTENSITY + 0.1)
        print(f"Glow intensity: {GLOW_INTENSITY:.1f}")
    elif key == ord('-') or key == ord('_'):
        GLOW_INTENSITY = max(1.0, GLOW_INTENSITY - 0.1)
        print(f"Glow intensity: {GLOW_INTENSITY:.1f}")

# Cleanup
pyautogui.keyUp('w')
pyautogui.keyUp('shift')
cap.release()
cv2.destroyAllWindows()
print("👋 System shutdown complete")
