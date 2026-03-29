"""
Subway Surfers Hand Gesture Controller
Author: Subash
GitHub: https://github.com/masssubash240
Control the game using finger gestures: 1 finger = jump, 2 fingers = slide, etc.
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math
from collections import deque

# ========== CONFIGURATION ==========
ACTION_COOLDOWN = 0.15          # Faster for gaming
SWIPE_THRESHOLD = 80
CONFIDENCE = 0.7
CAM_WIDTH, CAM_HEIGHT = 640, 480

# ========== MEDIAPIPE SETUP ==========
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=CONFIDENCE,
    min_tracking_confidence=0.5,
    max_num_hands=1
)

# ========== GLOBALS ==========
last_action_time = time.time()
gesture_history = deque(maxlen=5)
current_gesture = "NONE"
action_display = ""
action_display_time = 0
prev_hand_pos = None
last_swipe_time = time.time()

# Game stats (optional)
score = 0
high_score = 0

def count_fingers(hand_landmarks):
    """Return number of extended fingers (0-5)."""
    fingers = []
    landmarks = hand_landmarks.landmark
    
    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other 4 fingers
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip, pip in zip(tips, pips):
        if landmarks[tip].y < landmarks[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return sum(fingers)

def detect_swipe(current_pos, prev_pos):
    """Detect swipe direction for left/right moves."""
    global last_swipe_time
    if prev_pos is None:
        return None
    
    now = time.time()
    if now - last_swipe_time < 0.3:
        return None
    
    dx = current_pos[0] - prev_pos[0]
    dy = current_pos[1] - prev_pos[1]
    
    if abs(dx) < SWIPE_THRESHOLD and abs(dy) < SWIPE_THRESHOLD:
        return None
    
    if abs(dx) > abs(dy):
        return "RIGHT" if dx > 0 else "LEFT"
    else:
        return "DOWN" if dy > 0 else "UP"

def execute_game_command(finger_count, swipe_dir):
    """Send keyboard commands to Subway Surfers."""
    global last_action_time, action_display, action_display_time, score, high_score
    
    now = time.time()
    if now - last_action_time < ACTION_COOLDOWN:
        return
    
    command = None
    action_text = ""
    
    # Finger-based controls
    if finger_count == 1:
        pyautogui.press('up')
        action_text = "☝️ JUMP"
        score += 10
    elif finger_count == 2:
        pyautogui.press('down')
        action_text = "✌️ SLIDE"
        score += 5
    elif swipe_dir == "LEFT":
        pyautogui.press('left')
        action_text = "👈 LEFT"
        score += 5
    elif swipe_dir == "RIGHT":
        pyautogui.press('right')
        action_text = "👉 RIGHT"
        score += 5
    elif finger_count == 5:
        pyautogui.press('space')
        action_text = "✋ COLLECT POWER-UP"
        score += 20
    elif finger_count == 0:
        pyautogui.press('p')
        action_text = "⏸️ PAUSE"
    else:
        return
    
    # Update high score
    if score > high_score:
        high_score = score
    
    action_display = action_text
    action_display_time = now
    last_action_time = now
    print(f"[GAME] {action_text} | Score: {score}")

# ========== MAIN LOOP ==========
def main():
    global prev_hand_pos, score, high_score
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    
    print("=" * 60)
    print("🏃 SUBWAY SURFERS - HAND GESTURE CONTROLLER")
    print("=" * 60)
    print("\n🎮 CONTROLS:")
    print("  ☝️ 1 Finger        = JUMP (↑)")
    print("  ✌️ 2 Fingers       = SLIDE (↓)")
    print("  👈 Swipe Left      = MOVE LEFT (←)")
    print("  👉 Swipe Right     = MOVE RIGHT (→)")
    print("  ✋ Open Palm (5)    = COLLECT POWER-UP (Space)")
    print("  ✊ Fist (0)         = PAUSE GAME (P)")
    print("\n💡 TIPS:")
    print("  - Keep your hand in camera view")
    print("  - Make gestures clearly")
    print("  - Press 'r' to reset score")
    print("  - Press 'q' to quit")
    print("=" * 60)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        
        hand_center = None
        finger_count = 0
        swipe_dir = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2),
                    mp_drawing.DrawingSpec(color=(255,255,255), thickness=2)
                )
                
                # Get hand center (wrist)
                wrist = hand_landmarks.landmark[0]
                hand_center = (int(wrist.x * w), int(wrist.y * h))
                
                # Count fingers
                finger_count = count_fingers(hand_landmarks)
                
                # Detect swipe
                swipe_dir = detect_swipe(hand_center, prev_hand_pos)
                
                # Execute game command
                execute_game_command(finger_count, swipe_dir)
                
                # Display finger count
                cv2.putText(frame, f"Fingers: {finger_count}", (10, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                
                # Show swipe direction
                if swipe_dir:
                    cv2.putText(frame, f"Swipe: {swipe_dir}", (10, 80),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
                
                prev_hand_pos = hand_center
        else:
            prev_hand_pos = None
        
        # Draw HUD
        # Score and high score
        cv2.rectangle(frame, (0, 0), (w, 100), (0,0,0), -1)
        cv2.putText(frame, f"SCORE: {score}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,215,0), 2)
        cv2.putText(frame, f"HIGH: {high_score}", (20, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,215,0), 1)
        
        # Action feedback
        if time.time() - action_display_time < 0.5:
            scale = 1.2 + 0.3 * math.sin(time.time() * 20)
            tx = w//2 - 100
            ty = h//2 - 50
            cv2.rectangle(frame, (tx-10, ty-40), (tx+220, ty+20), (0,0,0), -1)
            cv2.putText(frame, action_display, (tx, ty),
                       cv2.FONT_HERSHEY_SIMPLEX, scale, (0,255,255), 3)
        
        # Help text
        cv2.putText(frame, "Press 'q' quit | 'r' reset score", (10, h-20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)
        
        cv2.imshow('Subway Surfers - Hand Controller', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            score = 0
            print("📊 Score reset!")
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n🏆 Game over! Final Score: {score} | High Score: {high_score}")

if __name__ == "__main__":
    main()
