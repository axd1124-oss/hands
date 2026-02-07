# hands
MediaPipe hand tracking with Open3D 3D visualization

## Overview
This project integrates MediaPipe for real-time hand tracking and Open3D for 3D visualization. It models detected hands using:
- **SPHERE** for the palm
- **CYLINDERS** for finger segments
- **Small spheres** for joints

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Test everything step-by-step
```bash
# Step 1: Validate dependencies
python test_dependencies.py

# Step 2: Test hand detection
python test_mediapipe.py

# Step 3: Test 3D visualization
python test_open3d.py

# Step 4: Run full hand model
python hand_model.py
```

📖 **See [SETUP.md](SETUP.md) for detailed step-by-step instructions and troubleshooting**

## Features
- ✅ Real-time hand detection using MediaPipe
- ✅ 3D hand model visualization with Open3D
- ✅ Finger segments represented as cylinders
- ✅ Palm represented as a sphere
- ✅ Joint markers at each landmark point
- ✅ Live camera feed with hand landmark overlay
- ✅ Save 3D models to `.ply` files
- ✅ Incremental testing scripts

## Hand Model Structure

```
PALM (wrist)
    └─ SPHERE (orange, radius: 0.04)
    
FINGERS (5 total)
    ├─ Thumb: 4 CYLINDER segments
    ├─ Index: 4 CYLINDER segments
    ├─ Middle: 4 CYLINDER segments
    ├─ Ring: 4 CYLINDER segments
    └─ Pinky: 4 CYLINDER segments
    
JOINTS (21 total)
    └─ Small SPHERES at each landmark
```

## Controls
- **'q'**: Quit the application
- **'s'**: Save the current 3D hand model as `hand_model.ply`

## Requirements
- Python 3.7+
- Webcam
- mediapipe==0.10.9
- opencv-python==4.9.0.80
- open3d==0.18.0
- numpy==1.24.3

## How It Works
1. **MediaPipe** captures hand landmarks from webcam feed (21 landmarks per hand)
2. Each landmark has 3D coordinates (x, y, z)
3. **Open3D** visualizes the hand as:
   - A SPHERE at the wrist (palm approximation)
   - CYLINDERS connecting each pair of landmarks (finger segments)
   - Small SPHERES at each joint

## File Structure
```
hands/
├── requirements.txt          # Dependencies
├── test_dependencies.py      # Step 1: Validate installation
├── test_mediapipe.py        # Step 2: Test hand detection
├── test_open3d.py           # Step 3: Test 3D visualization
├── hand_model.py            # Step 4: Full application
├── SETUP.md                 # Detailed setup guide
└── README.md                # This file
```

## Troubleshooting

See [SETUP.md](SETUP.md) for detailed troubleshooting steps.

Common issues:
- **Webcam not opening**: Close other apps using the camera
- **No hand detected**: Ensure good lighting and hand is visible
- **Import errors**: Run `pip install -r requirements.txt` again

## Credits
mediapipe testing + potential tartanhacks submission
