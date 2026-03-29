# Hand--Gesture-Gaming-Suite
# 🏃 Subway Surfers – Hand Gesture Controller

Control **Subway Surfers** using only your hand gestures – no keyboard needed!

![Demo](demo.gif)

## ✨ Features

- ☝️ **1 Finger** → Jump (↑)
- ✌️ **2 Fingers** → Slide (↓)
- 👈 **Swipe Left** → Move Left (←)
- 👉 **Swipe Right** → Move Right (→)
- ✋ **Open Palm (5 fingers)** → Collect Power-up (Space)
- ✊ **Fist (0 fingers)** → Pause Game (P)

## 🎮 Demo

[Add a short GIF or video here showing you playing Subway Surfers with hand gestures]

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/masssubash240/Subway-Surfers-Hand-Control.git
   cd Subway-Surfers-Hand-Control


# 🏎️ Car Racing Game – Hand Gesture Controller

**Complete Python code + GitHub-ready README files**

Control any car racing game using **hand gestures** – turn your hands into a virtual steering wheel!

---

## 🎮 Gesture Controls

| Gesture | Action | Game Control |
|---------|--------|--------------|
| 👐 **Hands Tilt Left** | Steer Left | `A` key (tap) |
| 👐 **Hands Tilt Right** | Steer Right | `D` key (tap) |
| 👍 **Left Thumb DOWN** | Accelerate | `W` key (hold) |
| 👍 **Left Thumb UP** | Stop Accelerating | Release `W` |
| 👎 **Right Thumb DOWN** | Brake/Reverse | `S` key (hold) |
| 👎 **Right Thumb UP** | Stop Braking | Release `S` |
| ✊ **Fist (0 fingers)** | Pause Game | `P` key |

---

## 📦 1. Complete Python Code

Save as `car_racing_controller.py`

```python
"""
Car Racing Game – Hand Gesture Controller
Author: Subash
GitHub: https://github.com/masssubash240
Control racing games using hand gestures: tilt hands to steer, thumbs for gas/brake!
Compatible with: Need for Speed, Forza, Asphalt, any game using WASD keys.
"""


---

## 2. 📄 GitHub README.md

Save this as `README.md` in your repository:

```markdown
# 🏎️ Hand Gesture Car Racing Controller

Control any car racing game using **hand gestures** – turn your hands into a virtual steering wheel!

![Demo](demo.gif)

## ✨ Features

| Gesture | Action | Game Control |
|---------|--------|--------------|
| 👐 **Hands Tilt Left** | Steer Left | `A` key (tap) |
| 👐 **Hands Tilt Right** | Steer Right | `D` key (tap) |
| 👍 **Left Thumb DOWN** | Accelerate | `W` key (hold) |
| 👍 **Left Thumb UP** | Stop Accelerating | Release `W` |
| 👎 **Right Thumb DOWN** | Brake/Reverse | `S` key (hold) |
| 👎 **Right Thumb UP** | Stop Braking | Release `S` |
| ✊ **Fist (hold 1s)** | Pause Game | `P` key |

## 🎮 Compatible Games

- Need for Speed series
- Forza Horizon
- Asphalt series
- Any racing game that uses WASD keys

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/masssubash240/Hand-Gesture-Car-Racing.git
   cd Hand-Gesture-Car-Racing
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the controller**
   ```bash
   python car_racing_controller.py
   ```

4. **Open your racing game** and position the window

5. **Show both hands to the webcam** and start racing!

## 🖥️ Requirements

- Python 3.7+
- Webcam (built-in or external)
- Windows / macOS / Linux

## 🎯 How It Works

- **MediaPipe** tracks both hands in real-time
- **Steering:** The angle between your hands determines left/right turns
- **Throttle:** Left thumb down = accelerate, up = stop
- **Brake:** Right thumb down = brake, up = stop
- **PyAutoGUI** sends keyboard inputs to the game

## ⚙️ Customization

Edit these variables in the code to adjust sensitivity:

```python
STRAIGHT_THRESHOLD = 6    # Degrees (±6° is straight)
TAP_DURATION = 0.02       # Turn tap duration (seconds)
ACTION_COOLDOWN = 0.05    # Min time between actions
```

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Game not responding | Click on the game window to focus it |
| Steering too sensitive | Increase `STRAIGHT_THRESHOLD` |
| Steering not responsive | Decrease `STRAIGHT_THRESHOLD` |
| Hands not detected | Improve lighting, use plain background |
| Lag | Lower camera resolution in code |

## 📁 Repository Structure

```
Hand-Gesture-Car-Racing/
├── car_racing_controller.py   # Main script
├── requirements.txt            # Dependencies
├── README.md                   # This file
└── demo.gif                    # Demo recording
```

## 🚀 Future Improvements

- [ ] Add on-screen steering wheel visualization
- [ ] Support for gear shifting gestures
- [ ] Profile system for different games
- [ ] Hand calibration mode

## 🤝 Contributing

Pull requests are welcome! Feel free to add new features or improve detection.

## 📝 License

MIT

## 👨‍💻 Author

**Subash** – [GitHub](https://github.com/masssubash240)

---

⭐ Star this repo if you find it useful!
```

---

## 3. 📦 requirements.txt

```txt
opencv-python==4.9.0.80
mediapipe==0.10.9
pyautogui==0.9.54
numpy==1.24.3
```

---

## 4. 🚀 Upload to GitHub

```bash
# Create folder and files
mkdir Hand-Gesture-Car-Racing
cd Hand-Gesture-Car-Racing

# Create the files (copy code above)
# car_racing_controller.py
# README.md
# requirements.txt

# Initialize git
git init
git add .
git commit -m "Initial commit: Hand gesture car racing controller"

# Connect to your GitHub repo
git remote add origin https://github.com/masssubash240/Hand-Gesture-Car-Racing.git
git branch -M main
git push -u origin main
```

---

## 🎮 Tips for Best Results

1. **Position your hands at shoulder width** – This gives the best angle detection
2. **Keep both hands visible** – The system needs both hands for steering
3. **Tilt like a steering wheel** – Don't move hands apart, tilt them together
4. **Good lighting** – MediaPipe works best in well-lit conditions
5. **Plain background** – Reduces false detections

---

## 📊 How the Steering Angle Works

```
Hands position visualization:

    LEFT TURN              STRAIGHT             RIGHT TURN
    \                      |                    /
     \    Left Hand    Left Hand    Right Hand    /
      \      ●              ●           ●       /
       \____________________|__________________/
```

- **Angle < -6°** → Turn Left (A key tap)
- **Angle between -6° and +6°** → Straight (no input)
- **Angle > +6°** → Turn Right (D key tap)

---

You're all set, Subash! Now your GitHub will have **three awesome gesture‑control projects**:

1. 🖐️ **Hand Gesture System Control** – Lock screen, volume, media
2. 🏃 **Subway Surfers Controller** – Jump, slide, collect
3. 🏎️ **Car Racing Controller** – Steer, accelerate, brake

Want me to also create a **YouTube video script** explaining this car racing project for your portfolio? 👊
