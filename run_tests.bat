@echo off
REM Quick Start Script for Hand Model (Windows)
REM Run this to test everything step-by-step

echo ==========================================
echo Hand Model - Quick Start
echo ==========================================
echo.

REM Check if requirements are installed
echo Step 1: Testing Dependencies...
python test_dependencies.py
if errorlevel 1 (
    echo.
    echo X Dependencies not installed properly!
    echo Run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo Press Enter to continue to Step 2 (MediaPipe test)...
pause >nul

echo.
echo Step 2: Testing MediaPipe Hand Detection...
echo Press 'q' in the window to continue to next step
python test_mediapipe.py

echo.
echo Press Enter to continue to Step 3 (Open3D test)...
pause >nul

echo.
echo Step 3: Testing Open3D 3D Visualization...
echo Close the 3D window to continue
python test_open3d.py

echo.
echo Press Enter to run the FULL HAND MODEL...
pause >nul

echo.
echo Step 4: Running Full Hand Model...
echo Press 'q' to quit, 's' to save model
python hand_model.py

echo.
echo ==========================================
echo All tests completed!
echo ==========================================
pause
