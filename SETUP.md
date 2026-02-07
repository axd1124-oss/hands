# Setup and Testing Guide

This guide will help you set up and test the hand tracking application step-by-step.

## Prerequisites

- Python 3.7 or higher
- Webcam
- Internet connection (for initial setup)

## Step-by-Step Setup

### Step 1: Install Dependencies

First, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- **mediapipe** - For hand tracking and landmark detection
- **opencv-python** - For webcam access and video processing
- **open3d** - For 3D visualization
- **numpy** - For numerical operations

### Step 2: Validate Installation

Run the dependency validation script to ensure everything is installed correctly:

```bash
python test_dependencies.py
```

**Expected Output:**
```
✓ mediapipe is installed
✓ opencv-python is installed
✓ open3d is installed
✓ numpy is installed
✓ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!
```

If you see any `✗` marks, the script will tell you what's missing.

---

### Step 3: Test Hand Detection (MediaPipe)

Test that MediaPipe can detect your hand from the webcam:

```bash
python test_mediapipe.py
```

**What to expect:**
- A window will open showing your webcam feed
- Show your hand to the camera
- You should see green dots (landmarks) and red lines (connections) on your hand
- The script will show detection statistics

**Controls:**
- Press `q` to quit

**Success criteria:**
- Green landmarks appear on your hand
- Detection rate > 50%

---

### Step 4: Test 3D Visualization (Open3D)

Test that Open3D can display 3D objects:

```bash
python test_open3d.py
```

**What to expect:**
- A 3D visualization window will open
- You should see a sample hand model:
  - Orange sphere (palm)
  - Colored cylinders (fingers)
  - Small spheres (joints)
- You can rotate, zoom, and pan with your mouse

**Controls:**
- **Left mouse** - Rotate
- **Scroll wheel** - Zoom
- **Right mouse** - Pan
- Close window to continue

**Success criteria:**
- 3D window opens without errors
- Hand model is visible and can be manipulated

---

### Step 5: Run the Full Hand Model

Now run the complete application:

```bash
python hand_model.py
```

**What to expect:**
- Two windows will open:
  1. **"Hand Tracking"** - Camera feed with hand landmarks
  2. **"3D Hand Model"** - 3D visualization of your hand

**How it works:**
- Show your hand to the camera
- The 3D window will display your hand as:
  - **SPHERE** for the palm
  - **CYLINDERS** for finger segments
  - **Small spheres** for joints
- Move your hand and watch the 3D model update in real-time!

**Controls:**
- `q` - Quit the application
- `s` - Save current 3D hand model to `hand_model.ply`

---

## Troubleshooting

### Problem: "Could not open webcam"
**Solution:** 
- Make sure your webcam is connected
- Close other applications using the webcam (Zoom, Skype, etc.)
- Try running with administrator/sudo privileges

### Problem: "No hand detected"
**Solution:**
- Make sure your hand is clearly visible to the camera
- Ensure good lighting
- Keep your hand within the camera frame
- Try different hand positions and distances

### Problem: "ImportError" or missing modules
**Solution:**
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.7+
- Try creating a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

### Problem: 3D window is black or frozen
**Solution:**
- Update your graphics drivers
- Try running on a different machine
- Check Open3D installation: `pip install --upgrade open3d`

---

## Understanding the Hand Model

The 3D hand model consists of:

### Palm
- Represented as a **sphere** at the wrist landmark (landmark 0)
- Color: Orange (0.9, 0.6, 0.3)
- Radius: 0.04 units

### Fingers
Each finger has **4 segments** represented as cylinders:
1. **Thumb** - 4 segments
2. **Index finger** - 4 segments  
3. **Middle finger** - 4 segments
4. **Ring finger** - 4 segments
5. **Pinky** - 4 segments

### Joints
- Small **spheres** at each of the 21 hand landmarks
- Color: Reddish-brown (0.7, 0.3, 0.1)
- Radius: 0.01 units

### Color Scheme
- Different fingers have slightly different colors for easy identification
- Fingers transition from reddish to brownish

---

## Next Steps

Once everything is working:
1. Experiment with different hand gestures
2. Try both hands (change `max_num_hands` in code)
3. Save interesting hand poses with the `s` key
4. Modify colors and sizes in the code
5. Add new features!

---

## File Overview

- `requirements.txt` - Dependencies list
- `test_dependencies.py` - Validates all dependencies are installed
- `test_mediapipe.py` - Tests hand detection only
- `test_open3d.py` - Tests 3D visualization only
- `hand_model.py` - Full hand tracking and modeling application
- `SETUP.md` - This guide

---

**Enjoy tracking your hands in 3D!**
