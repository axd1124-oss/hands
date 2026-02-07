#!/bin/bash
# Quick Start Script for Hand Model
# Run this to test everything step-by-step

echo "=========================================="
echo "Hand Model - Quick Start"
echo "=========================================="
echo ""

# Check if requirements are installed
echo "Step 1: Testing Dependencies..."
python test_dependencies.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Dependencies not installed properly!"
    echo "Run: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "Press Enter to continue to Step 2 (MediaPipe test)..."
read

echo ""
echo "Step 2: Testing MediaPipe Hand Detection..."
echo "Press 'q' in the window to continue to next step"
python test_mediapipe.py

echo ""
echo "Press Enter to continue to Step 3 (Open3D test)..."
read

echo ""
echo "Step 3: Testing Open3D 3D Visualization..."
echo "Close the 3D window to continue"
python test_open3d.py

echo ""
echo "Press Enter to run the FULL HAND MODEL..."
read

echo ""
echo "Step 4: Running Full Hand Model..."
echo "Press 'q' to quit, 's' to save model"
python hand_model.py

echo ""
echo "=========================================="
echo "✅ All tests completed!"
echo "=========================================="
