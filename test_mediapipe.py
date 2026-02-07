"""
Step 2: Test MediaPipe Hand Detection
This script tests ONLY the hand detection using MediaPipe.
It displays the webcam feed with hand landmarks overlaid.
"""

import cv2
import mediapipe as mp
import sys

def test_mediapipe():
    """Test MediaPipe hand detection."""
    print("=" * 60)
    print("TESTING MEDIAPIPE HAND DETECTION")
    print("=" * 60)
    print()
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    print("✓ MediaPipe Hands initialized")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ Error: Could not open webcam")
        print("Make sure your webcam is connected and not in use by another application")
        sys.exit(1)
    
    print("✓ Webcam opened successfully")
    print()
    print("Instructions:")
    print("  - Show your hand to the camera")
    print("  - You should see landmarks (dots and lines) on your hand")
    print("  - Press 'q' to quit and proceed to next test")
    print()
    
    frame_count = 0
    detection_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("✗ Error: Could not read frame from webcam")
                break
            
            frame_count += 1
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = hands.process(rgb_frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                detection_count += 1
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks and connections
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
                    
                    # Display landmark count
                    cv2.putText(frame, f"Landmarks: 21 detected", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No hand detected", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Display frame info
            detection_rate = (detection_count / frame_count) * 100 if frame_count > 0 else 0
            cv2.putText(frame, f"Detection Rate: {detection_rate:.1f}%", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow('MediaPipe Hand Detection Test', frame)
            
            # Check for 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        # Cleanup
        hands.close()
        cap.release()
        cv2.destroyAllWindows()
        
        print()
        print("=" * 60)
        print("MEDIAPIPE TEST RESULTS")
        print("=" * 60)
        print(f"Total frames processed: {frame_count}")
        print(f"Frames with hand detected: {detection_count}")
        print(f"Detection rate: {detection_rate:.1f}%")
        
        if detection_count > 0:
            print()
            print("✓ MediaPipe hand detection is working!")
            print()
            print("Next step:")
            print("  Run: python test_open3d.py (test 3D visualization)")
        else:
            print()
            print("⚠ Warning: No hands were detected")
            print("  Make sure to show your hand clearly to the camera")
        print("=" * 60)

if __name__ == "__main__":
    test_mediapipe()
