# hands
MediaPipe hand tracking with Open3D 3D visualization

## Overview
This project integrates MediaPipe for real-time hand tracking and Open3D for 3D visualization. It models detected hands using:
- **Cylinders** for finger segments
- **Sphere** for the palm
- **Small spheres** for joints

## Installation

1. Clone the repository:
```bash
git clone https://github.com/axd1124-oss/hands.git
cd hands
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the hand tracking application:
```bash
python hand_tracking_3d.py
```

### Controls
- **'q'**: Quit the application
- **'s'**: Save the current 3D hand model as `hand_model.ply`

### Features
- Real-time hand detection using MediaPipe
- 3D hand model visualization with Open3D
- Finger segments represented as cylinders
- Palm represented as a sphere
- Joint markers at each landmark point
- Live camera feed with hand landmark overlay

## Requirements
- Python 3.7+
- Webcam
- mediapipe
- opencv-python
- open3d
- numpy

## How It Works
1. **MediaPipe** captures hand landmarks from webcam feed (21 landmarks per hand)
2. Each landmark has 3D coordinates (x, y, z)
3. **Open3D** visualizes the hand as:
   - A sphere at the wrist (palm approximation)
   - Cylinders connecting each pair of landmarks (finger segments)
   - Small spheres at each joint

## Credits
mediapipe testing + potential tartanhacks submission
