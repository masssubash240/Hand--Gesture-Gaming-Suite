import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math
from collections import deque

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.7,
    max_num_hands=2  # Support for two hands
)

# Game control variables
accelerating = False
braking = False
nitro_active = False
last_action_time = time.time()
action_cooldown = 0.1  # Faster response for racing game

# Gesture tracking
gesture_history = deque(maxlen=3)
hand_positions = deque(maxlen=5)

# Gas control (0-100%)
gas_percentage = 0
target_gas = 0

# Action feedback
current_action = ""
action_display_time = 0
game_score = 0

# Timer for special actions
restart_timer = None
pause_timer = None

def count_fingers(hand_landmarks):
    """Count extended fingers"""
    fingers = []
    landmarks = hand_landmarks.landmark
    
    # Thumb
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    
    if thumb_tip.x < thumb_ip.x:  # Right hand
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other fingers
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    for tip_id, pip_id in zip(finger_tips, finger_pips):
        if landmarks[tip_id].y < landmarks[pip_id].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return sum(fingers)

def get_hand_height(hand_landmarks, frame_height):
    """Get hand height for gas control"""
    wrist = hand_landmarks.landmark[0]
    return int(wrist.y * frame_height)

def detect_pinch(hand_landmarks):
    """Detect pinch gesture for reset"""
    landmarks = hand_landmarks.landmark
    
    thumb_index_dist = math.hypot(
        landmarks[4].x - landmarks[8].x,
        landmarks[4].y - landmarks[8].y
    )
    
    return thumb_index_dist < 0.05

def execute_hill_climb_command(gesture_info):
    """Execute game commands for Hill Climb Racing"""
    global last_action_time, current_action, action_display_time
    global accelerating, braking, gas_percentage, target_gas
    global nitro_active, restart_timer, pause_timer, game_score
    
    finger_count = gesture_info['finger_count']
    hand_height = gesture_info['hand_height']
    frame_height = gesture_info['frame_height']
    pinch_detected = gesture_info['pinch']
    two_hands = gesture_info['two_hands']
    
    current_time = time.time()
    
    # 🎮 MAIN CONTROLS
    
    # FIST (0 fingers) = ACCELERATE
    if finger_count == 0 and not two_hands:
        if not accelerating:
            pyautogui.keyDown('up')
            accelerating = True
            current_action = "⚡ GAS"
            action_display_time = current_time
            print("⚡ Accelerating!")
        
        # Variable gas based on hand height
        target_gas = np.interp(hand_height, [frame_height//2, 100], [50, 100])
        gas_percentage = target_gas
        game_score += 1
    
    # OPEN PALM (5 fingers) = BRAKE/REVERSE
    elif finger_count == 5 and not two_hands:
        if not braking:
            pyautogui.keyDown('down')
            braking = True
            if accelerating:
                pyautogui.keyUp('up')
                accelerating = False
            current_action = "🛑 BRAKE"
            action_display_time = current_time
            print("🛑 Braking!")
        gas_percentage = 0
    
    # THREE FINGERS (3) = BALANCE BACK (LEFT)
    elif finger_count == 3:
        pyautogui.press('left')
        current_action = "⬅️ BALANCE BACK"
        action_display_time = current_time
        last_action_time = current_time
        game_score += 5
    
    # FOUR FINGERS (4) = BALANCE FORWARD (RIGHT)
    elif finger_count == 4:
        pyautogui.press('right')
        current_action = "➡️ BALANCE FORWARD"
        action_display_time = current_time
        last_action_time = current_time
        game_score += 5
    
    # INDEX UP (1 finger) = NITRO/BOOST
    elif finger_count == 1:
        pyautogui.press('space')
        nitro_active = True
        current_action = "💨 NITRO BOOST!"
        action_display_time = current_time
        last_action_time = current_time
        game_score += 20
    
    # PEACE SIGN (2 fingers) = RESTART (with hold)
    elif finger_count == 2:
        if restart_timer is None:
            restart_timer = current_time
        elif current_time - restart_timer > 1.5:  # Hold 1.5 sec to restart
            pyautogui.press('r')
            current_action = "🔄 RESTARTING LEVEL"
            action_display_time = current_time
            print("🔄 Restarting level!")
            game_score = 0
            restart_timer = None
            last_action_time = current_time
    else:
        restart_timer = None
    
    # TWO HANDS DETECTED = PAUSE
    if two_hands:
        if pause_timer is None:
            pause_timer = current_time
        elif current_time - pause_timer > 1:  # Hold 1 sec to pause
            pyautogui.press('p')
            current_action = "⏸️ GAME PAUSED"
            action_display_time = current_time
            print("⏸️ Game Paused!")
            pause_timer = None
            last_action_time = current_time
    else:
        pause_timer = None
    
    # PINCH GESTURE = QUICK RESET
    if pinch_detected:
        pyautogui.press('r')
        current_action = "🔄 QUICK RESET"
        action_display_time = current_time
        last_action_time = current_time
        game_score = 0
    
    # Release keys if no gesture
    if finger_count != 0 and accelerating:
        pyautogui.keyUp('up')
        accelerating = False
    
    if finger_count != 5 and braking:
        pyautogui.keyUp('down')
        braking = False

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("=" * 60)
print("🚗 HILL CLIMB RACING - HAND GESTURE CONTROLLER")
print("=" * 60)
print("\n📋 GESTURE CONTROLS:")
print("  ✊ Fist            = ACCELERATE (Hold)")
print("  ✋ Open Palm       = BRAKE/REVERSE (Hold)")
print("  🤟 Three Fingers   = BALANCE BACK (←)")
print("  🖐️ Four Fingers    = BALANCE FORWARD (→)")
print("  ☝️ Index Up        = NITRO BOOST (␣)")
print("  ✌️ Peace Sign      = RESTART LEVEL (Hold 1.5s)")
print("  👊 Two Fists       = PAUSE GAME")
print("  🤏 Pinch           = QUICK RESET")
print("\n🎯 HAND POSITION:")
print("  👆 Hand Higher = More Gas")
print("  👇 Hand Lower  = Less Gas")
print("\n🎮 Press 'q' to quit | 'r' to reset score")
print("=" * 60)

# Game state
game_active = True
hand_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue
    
    # Flip frame
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    
    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Track number of hands
    hand_count = 0 if not results.multi_hand_landmarks else len(results.multi_hand_landmarks)
    
    # Gas gauge background
    gauge_x = 30
    gauge_y = 100
    gauge_width = 30
    gauge_height = 200
    
    # Draw gas gauge
    cv2.rectangle(frame, (gauge_x, gauge_y), 
                 (gauge_x + gauge_width, gauge_y + gauge_height), 
                 (50, 50, 50), -1)
    
    # Fill gas percentage
    fill_height = int((gas_percentage / 100) * gauge_height)
    if fill_height > 0:
        color = (0, 255, 0) if gas_percentage < 70 else (0, 255, 255) if gas_percentage < 90 else (0, 0, 255)
        cv2.rectangle(frame, 
                     (gauge_x, gauge_y + gauge_height - fill_height),
                     (gauge_x + gauge_width, gauge_y + gauge_height),
                     color, -1)
    
    # Gas percentage text
    cv2.putText(frame, f"GAS: {int(gas_percentage)}%", 
               (gauge_x - 10, gauge_y - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Draw hand landmarks with different colors for each hand
            color = (0, 255, 0) if i == 0 else (255, 0, 0)
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=2),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
            )
            
            # Count fingers for this hand
            finger_count = count_fingers(hand_landmarks)
            
            # Get hand height for gas control (use first hand only)
            hand_height = get_hand_height(hand_landmarks, frame_height)
            
            # Detect pinch
            pinch = detect_pinch(hand_landmarks)
            
            # Draw hand height indicator
            cv2.circle(frame, (frame_width - 50, hand_height), 10, (255, 255, 0), -1)
            cv2.line(frame, (frame_width - 70, hand_height), 
                    (frame_width - 30, hand_height), (255, 255, 0), 2)
            
            # Prepare gesture info
            gesture_info = {
                'finger_count': finger_count,
                'hand_height': hand_height,
                'frame_height': frame_height,
                'pinch': pinch,
                'two_hands': hand_count > 1
            }
            
            # Execute command if game is active
            if game_active:
                execute_hill_climb_command(gesture_info)
            
            # Draw finger count for each hand
            cv2.putText(frame, f"Hand {i+1}: {finger_count} fingers", 
                       (10, 50 + i*30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw pinch indicator
            if pinch:
                cv2.putText(frame, "🤏 PINCH", 
                           (frame_width - 150, 50 + i*30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    # Draw HUD
    
    # Game status
    status_color = (0, 255, 0) if game_active else (0, 0, 255)
    cv2.putText(frame, f"GAME: {'ACTIVE' if game_active else 'PAUSED'}", 
               (frame_width - 200, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    
    # Score
    cv2.putText(frame, f"SCORE: {game_score}", 
               (frame_width - 200, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 215, 0), 2)
    
    # Action feedback with animation
    if time.time() - action_display_time < 0.5:
        # Scale effect
        scale = 1.5 + 0.3 * math.sin(time.time() * 20)
        text_size = cv2.getTextSize(current_action, cv2.FONT_HERSHEY_SIMPLEX, scale, 3)[0]
        text_x = frame_width // 2 - text_size[0] // 2
        text_y = frame_height // 2 - 50
        
        # Background with gradient effect
        overlay = frame.copy()
        cv2.rectangle(overlay, 
                     (text_x - 20, text_y - text_size[1] - 20),
                     (text_x + text_size[0] + 20, text_y + 20),
                     (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(frame, current_action, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 0), 3)
    
    # Driving indicators
    if accelerating:
        cv2.putText(frame, "⚡ ACCELERATING", (frame_width//2 - 100, frame_height - 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif braking:
        cv2.putText(frame, "🛑 BRAKING", (frame_width//2 - 80, frame_height - 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    # Control guide overlay
    if hand_count == 0:
        cv2.putText(frame, "👆 SHOW YOUR HAND TO PLAY", 
                   (frame_width//2 - 200, frame_height//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Hand count
    cv2.putText(frame, f"Hands: {hand_count}", (10, frame_height - 20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Quick guide
    guide_y = frame_height - 100
    cv2.putText(frame, "✊ Gas | ✋ Brake | 🤟← | 🖐️→ | ☝️Nitro | ✌️Restart", 
               (10, guide_y),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Show frame
    cv2.imshow('Hill Climb Racing - Hand Controller', frame)
    
    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        game_score = 0
        print("📊 Score reset!")
    elif key == ord('p'):
        game_active = not game_active
        print(f"⏸️ Game {'Paused' if not game_active else 'Resumed'}")
        if not game_active:
            # Release all keys when paused
            if accelerating:
                pyautogui.keyUp('up')
                accelerating = False
            if braking:
                pyautogui.keyUp('down')
                braking = False

# Release keys on exit
if accelerating:
    pyautogui.keyUp('up')
if braking:
    pyautogui.keyUp('down')

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("\n" + "=" * 60)
print(f"🏁 GAME OVER! Final Score: {game_score}")
print("👋 Thanks for playing Hill Climb Racing!")
print("=" * 60)
