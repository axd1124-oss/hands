"""
Hand Tracking and 3D Modeling using MediaPipe and Open3D
This script captures hand landmarks using MediaPipe and visualizes them 
as a 3D model using Open3D with cylinders for fingers and a sphere for the palm.
"""

import cv2
import mediapipe as mp
import numpy as np
import open3d as o3d


class HandModel3D:
    """Creates and manages a 3D hand model using Open3D."""
    
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Define finger connections (landmark indices)
        self.finger_connections = [
            # Thumb
            [(0, 1), (1, 2), (2, 3), (3, 4)],
            # Index finger
            [(0, 5), (5, 6), (6, 7), (7, 8)],
            # Middle finger
            [(0, 9), (9, 10), (10, 11), (11, 12)],
            # Ring finger
            [(0, 13), (13, 14), (14, 15), (15, 16)],
            # Pinky
            [(0, 17), (17, 18), (18, 19), (19, 20)]
        ]
        
    def create_cylinder(self, start, end, radius=0.01, color=[0.8, 0.4, 0.2]):
        """Create a cylinder mesh between two points."""
        # Calculate cylinder height and direction
        direction = end - start
        height = np.linalg.norm(direction)
        
        if height < 1e-6:  # Avoid zero-length cylinders
            return None
            
        # Create cylinder along z-axis
        cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height)
        
        # Calculate rotation to align with direction
        z_axis = np.array([0, 0, 1])
        direction_normalized = direction / height
        
        # Calculate rotation axis and angle
        rotation_axis = np.cross(z_axis, direction_normalized)
        rotation_axis_norm = np.linalg.norm(rotation_axis)
        
        if rotation_axis_norm > 1e-6:
            rotation_axis = rotation_axis / rotation_axis_norm
            angle = np.arccos(np.clip(np.dot(z_axis, direction_normalized), -1.0, 1.0))
            
            # Create rotation matrix using Rodrigues' rotation formula
            K = np.array([
                [0, -rotation_axis[2], rotation_axis[1]],
                [rotation_axis[2], 0, -rotation_axis[0]],
                [-rotation_axis[1], rotation_axis[0], 0]
            ])
            R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
        else:
            # If direction is already aligned with z-axis (or opposite)
            if direction_normalized[2] < 0:
                R = np.diag([1, 1, -1])
            else:
                R = np.eye(3)
        
        # Apply rotation
        cylinder.rotate(R, center=[0, 0, 0])
        
        # Translate to position (center of cylinder should be at midpoint)
        cylinder.translate(start + direction / 2)
        
        # Set color
        cylinder.paint_uniform_color(color)
        
        return cylinder
    
    def create_sphere(self, center, radius=0.03, color=[0.9, 0.6, 0.3]):
        """Create a sphere mesh at a given position."""
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
        sphere.translate(center)
        sphere.paint_uniform_color(color)
        return sphere
    
    def create_hand_mesh(self, landmarks_3d):
        """Create a 3D hand model with cylinders for fingers and sphere for palm."""
        meshes = []
        
        # Create palm sphere at wrist (landmark 0)
        palm_center = landmarks_3d[0]
        palm_sphere = self.create_sphere(palm_center, radius=0.04, color=[0.9, 0.6, 0.3])
        meshes.append(palm_sphere)
        
        # Create cylinders for each finger segment
        for finger_idx, finger in enumerate(self.finger_connections):
            # Color varies slightly per finger
            color_variation = finger_idx * 0.1
            color = [0.8 - color_variation * 0.1, 0.4 + color_variation * 0.05, 0.2]
            
            for connection in finger:
                start_idx, end_idx = connection
                start = landmarks_3d[start_idx]
                end = landmarks_3d[end_idx]
                
                cylinder = self.create_cylinder(start, end, radius=0.008, color=color)
                if cylinder is not None:
                    meshes.append(cylinder)
        
        # Create small spheres at each joint
        for i, landmark in enumerate(landmarks_3d):
            if i > 0:  # Skip wrist, already have palm sphere
                joint_sphere = self.create_sphere(landmark, radius=0.01, color=[0.7, 0.3, 0.1])
                meshes.append(joint_sphere)
        
        return meshes
    
    def process_frame(self, frame):
        """Process a frame and return hand landmarks."""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = self.hands.process(rgb_frame)
        
        # Draw on frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                
                # Extract 3D landmarks
                landmarks_3d = []
                for landmark in hand_landmarks.landmark:
                    landmarks_3d.append(np.array([landmark.x, landmark.y, landmark.z]))
                
                return frame, np.array(landmarks_3d)
        
        return frame, None
    
    def cleanup(self):
        """Release resources."""
        self.hands.close()


def main():
    """Main function to run hand tracking and 3D visualization."""
    # Initialize hand model
    hand_model = HandModel3D()
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print("Hand Tracking with 3D Visualization")
    print("Press 'q' to quit")
    print("Press 's' to save current 3D model")
    
    # Create Open3D visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="3D Hand Model", width=800, height=600)
    
    # Add coordinate frame for reference
    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
    vis.add_geometry(coord_frame)
    
    current_meshes = []
    first_frame = True
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            # Process frame
            frame, landmarks_3d = hand_model.process_frame(frame)
            
            # Update 3D visualization
            if landmarks_3d is not None:
                # Remove old meshes
                for mesh in current_meshes:
                    vis.remove_geometry(mesh, reset_bounding_box=False)
                current_meshes.clear()
                
                # Create new hand mesh
                new_meshes = hand_model.create_hand_mesh(landmarks_3d)
                current_meshes = new_meshes
                
                # Add new meshes
                for mesh in current_meshes:
                    vis.add_geometry(mesh, reset_bounding_box=first_frame)
                
                if first_frame:
                    vis.reset_view_point(True)
                    first_frame = False
            
            # Update visualizer
            vis.poll_events()
            vis.update_renderer()
            
            # Show camera feed
            cv2.imshow('Hand Tracking', frame)
            
            # Check for key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and landmarks_3d is not None:
                # Save current 3D model
                combined_mesh = o3d.geometry.TriangleMesh()
                for mesh in current_meshes:
                    combined_mesh += mesh
                o3d.io.write_triangle_mesh("hand_model.ply", combined_mesh)
                print("Saved 3D hand model to 'hand_model.ply'")
    
    finally:
        # Cleanup
        hand_model.cleanup()
        cap.release()
        cv2.destroyAllWindows()
        vis.destroy_window()


if __name__ == "__main__":
    main()
