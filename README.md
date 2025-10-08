# YourVision

YourVision is a collection of games and tools made using computer vision techniques. Each application provides interactive and engaging experiences.

## Included Applications

- **DanceWithMe** - A fun game where your dance moves or body movements are mimicked by a stickman.
- **HandMouse** - Control your mouse using hand gestures.
- **FaceBlur** - A privacy tool that detects and blurs faces in real-time video.
- **FoodEater** - Eat foods coming through the screen by opening your mouth.
- **RedLightGreenLight** - A representation game inspired by *Squid Game*, where you move when the light is green and freeze when it's red.
- **MyAvatar** - Create a cartoonized or stylized avatar of yourself using your webcam.

---

## Installation

1. Ensure **Python 3.10** is installed on your system. You can download it from [python.org](https://www.python.org/).
   > Note: Versions other than 3.10 may not work due to compatibility issues with some libraries like `mediapipe`.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### **FaceBlur**
A privacy tool that detects and blurs faces in real-time video. You can toggle blur modes, capture screenshots, and record videos using keyboard inputs.

```bash
python blurface.py
```

**Controls:**
- `q` : Quit program
- `s` : Toggle between Gaussian and Pixelate blur
- `f` : Toggle detection rectangle
- `p` : Pause/resume video
- `r` : Start/stop recording
- `c` : Capture a snapshot

> Note: May lag on low-end PCs. If fps is low, try restarting or changing blur methods.

---

### **HandMouse**
Control your mouse using hand gestures. Make a fist for left click/drag and thumbs up for right click.

```bash
python handmouse.py
```

**Controls:**
- `q` : Quit program

---

### **DanceWithMe**
Your dance moves are mimicked by a stickman. Capture snapshots or record your dance moves.

```bash
python dancewithme.py
```

**Controls:**
- `q` : Quit program
- `s` : Capture snapshot
- `r` : Start/stop recording

> Make sure to have fun and dance!

---

### **FoodEater**
Eat foods coming through the screen by opening your mouth. You have 3 lives; the game becomes progressively harder.

```bash
python foodeater.py
```

**Controls:**
- `q` : Quit program

> Ensure your face is well-lit and clearly visible for best results.

---

### **MyAvatar**
Create a cartoonized or stylized avatar of yourself in real-time.

```bash
python myavatar.py
```

**Controls:**
- `q` : Quit program
- `s` : Save snapshot of cartoonized avatar
- `c` : Save snapshot of stylized avatar

> Ensure your face is well-lit and clearly visible for best results.

---

### **RedLightGreenLight**
A game inspired by *Squid Game*. Move when the light is green and freeze when it's red. Tracks your knee movements to detect motion. Complete the running gesture threshold within the time limit. Difficulty increases as levels progress.

```bash
python Red_Light_Green_Light.py
```

**Controls:**
- `q` : Quit program

> Ensure your full body is visible to the camera for best results.

---

## License
[MIT](LICENSE)