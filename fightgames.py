"""
Fighting Game Hand Gesture Controller (Tekken / Street Fighter)
Author: Subash
GitHub: https://github.com/masssubash240
Control fighting games using 1,2,3,4 fingers and swipes.
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math
from collections import deque

# ========== CONFIGURATION ==========
ACTION_COOLDOWN = 0.15          # Seconds between actions
SWIPE_THRESHOLD = 70            # Pixels for swipe detection
SWIPE_COOLDOWN = 0.3            # Seconds between swipes
CONFIDENCE = 0.7
CAM_WIDTH, CAM_HEIGHT = 640, 480

# Key mappings (change according to your game)
KEYS = {
    "1_FINGER": "j",        # Light punch
    "2_FINGERS": "k",       # Light kick
    "3_FINGERS": "u",       # Heavy punch
    "4_FINGERS": "i",       # Heavy kick
    "FIST": "o",            # Block
    "OPEN_PALM": "p",       # Super
    "SWIPE_LEFT": "a",      # Move left
    "SWIPE_RIGHT": "d",     # Move right
    "SWIPE_UP": "w",        # Jump
    "SWIPE_DOWN": "s",      # Crouch
}

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
last_swipe_time = time.time()
gesture_history = deque(maxlen=5)
current_gesture = "NONE"
action_display = ""
action_display_time = 0
prev_hand_pos = None

# Game stats (optional)
combo_counter = 0
score = 0

def count_fingers(hand_landmarks):
    """Return number of extended fingers (0-5)."""
    fingers = []
    landmarks = hand_landmarks.landmark
    
    # Thumb (special logic for right hand)
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
    """Detect swipe direction based on hand movement."""
    global last_swipe_time
    if prev_pos is None:
        return None
    
    now = time.time()
    if now - last_swipe_time < SWIPE_COOLDOWN:
        return None
    
    dx = current_pos[0] - prev_pos[0]
    dy = current_pos[1] - prev_pos[1]
    
    if abs(dx) < SWIPE_THRESHOLD and abs(dy) < SWIPE_THRESHOLD:
        return None
    
    if abs(dx) > abs(dy):
        return "RIGHT" if dx > 0 else "LEFT"
    else:
        return "DOWN" if dy > 0 else "UP"

def execute_fighting_command(finger_count, swipe_dir):
    """Send keyboard commands to fighting game."""
    global last_action_time, action_display, action_display_time, combo_counter, score
    
    now = time.time()
    if now - last_action_time < ACTION_COOLDOWN:
        return
    
    key = None
    action_text = ""
    is_swipe = False
    
    # Finger-based attacks
    if finger_count == 1:
        key = KEYS["1_FINGER"]
        action_text = "☝️ LIGHT PUNCH"
        combo_counter += 1
        score += 10
    elif finger_count == 2:
        key = KEYS["2_FINGERS"]
        action_text = "✌️ LIGHT KICK"
        combo_counter += 1
        score += 10
    elif finger_count == 3:
        key = KEYS["3_FINGERS"]
        action_text = "🤟 HEAVY PUNCH"
        combo_counter += 2
        score += 20
    elif finger_count == 4:
        key = KEYS["4_FINGERS"]
        action_text = "🖐️ HEAVY KICK"
        combo_counter += 2
        score += 20
    elif finger_count == 0:
        key = KEYS["FIST"]
        action_text = "✊ BLOCK"
        combo_counter = 0
        score += 5
    elif finger_count == 5:
        key = KEYS["OPEN_PALM"]
        action_text = "✋ SUPER ATTACK!"
        combo_counter = 0
        score += 50
    # Swipe movements
    elif swipe_dir == "LEFT":
        key = KEYS["SWIPE_LEFT"]
        action_text = "👈 MOVE LEFT"
        is_swipe = True
    elif swipe_dir == "RIGHT":
        key = KEYS["SWIPE_RIGHT"]
        action_text = "👉 MOVE RIGHT"
        is_swipe = True
    elif swipe_dir == "UP":
        key = KEYS["SWIPE_UP"]
        action_text = "👆 JUMP"
        is_swipe = True
    elif swipe_dir == "DOWN":
        key = KEYS["SWIPE_DOWN"]
        action_text = "👇 CROUCH"
        is_swipe = True
    else:
        return
    
    # Send key press (tap for swipes, tap for attacks)
    if key:
        pyautogui.press(key)
        print(f"[FIGHT] {action_text} -> Key: {key}")
    
    action_display = action_text
    action_display_time = now
    last_action_time = now

# ========== MAIN LOOP ==========
def main():
    global prev_hand_pos, combo_counter, score
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    
    print("=" * 60)
    print("🥊 FIGHTING GAME - HAND GESTURE CONTROLLER")
    print("=" * 60)
    print("\n🎮 CONTROLS:")
    print("  ☝️ 1 Finger        = Light Punch (J)")
    print("  ✌️ 2 Fingers       = Light Kick (K)")
    print("  🤟 3 Fingers       = Heavy Punch (U)")
    print("  🖐️ 4 Fingers       = Heavy Kick (I)")
    print("  ✊ Fist            = Block (O)")
    print("  ✋ Open Palm (5)    = Super Attack (P)")
    print("  👈 Swipe Left      = Move Left (A)")
    print("  👉 Swipe Right     = Move Right (D)")
    print("  👆 Swipe Up        = Jump (W)")
    print("  👇 Swipe Down      = Crouch (S)")
    print("\n💡 TIPS:")
    print("  - Keep hand in camera view")
    print("  - Use clear finger counts")
    print("  - Swipe quickly for movements")
    print("  - Press 'r' to reset combo/score")
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
                
                # Execute command
                execute_fighting_command(finger_count, swipe_dir)
                
                # Draw finger count
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
        # Semi-transparent top bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 100), (0,0,0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Score and combo
        cv2.putText(frame, f"SCORE: {score}", (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,215,0), 2)
        cv2.putText(frame, f"COMBO: x{combo_counter}", (20, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
        
        # Action feedback with animation
        if time.time() - action_display_time < 0.4:
            scale = 1.2 + 0.3 * math.sin(time.time() * 25)
            tx = w//2 - 120
            ty = h//2 - 50
            cv2.rectangle(frame, (tx-10, ty-35), (tx+250, ty+15), (0,0,0), -1)
            cv2.putText(frame, action_display, (tx, ty),
                       cv2.FONT_HERSHEY_SIMPLEX, scale, (0,255,255), 3)
        
        # Help text
        cv2.putText(frame, "1☝️ 2✌️ 3🤟 4🖐️ | Swipe moves | 'q' quit | 'r' reset", (10, h-20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)
        
        cv2.imshow('Fighting Game - Hand Controller', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            combo_counter = 0
            score = 0
            print("📊 Combo and score reset!")
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n🏆 Final Score: {score} | Max Combo: {combo_counter}")

if __name__ == "__main__":
    main()
