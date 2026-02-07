"""
Step 3: Test Open3D 3D Visualization
This script tests ONLY the Open3D visualization with a sample hand model.
It creates a simple 3D hand structure to verify Open3D is working.
"""

import open3d as o3d
import numpy as np
import sys

def create_cylinder(start, end, radius=0.01, color=[0.8, 0.4, 0.2]):
    """Create a cylinder mesh between two points."""
    direction = end - start
    height = np.linalg.norm(direction)
    
    if height < 1e-6:
        return None
    
    # Create cylinder along z-axis
    cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height)
    
    # Calculate rotation
    z_axis = np.array([0, 0, 1])
    direction_normalized = direction / height
    
    rotation_axis = np.cross(z_axis, direction_normalized)
    rotation_axis_norm = np.linalg.norm(rotation_axis)
    
    if rotation_axis_norm > 1e-6:
        rotation_axis = rotation_axis / rotation_axis_norm
        angle = np.arccos(np.clip(np.dot(z_axis, direction_normalized), -1.0, 1.0))
        
        K = np.array([
            [0, -rotation_axis[2], rotation_axis[1]],
            [rotation_axis[2], 0, -rotation_axis[0]],
            [-rotation_axis[1], rotation_axis[0], 0]
        ])
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
    else:
        if direction_normalized[2] < 0:
            R = np.diag([1, 1, -1])
        else:
            R = np.eye(3)
    
    cylinder.rotate(R, center=[0, 0, 0])
    cylinder.translate(start + direction / 2)
    cylinder.paint_uniform_color(color)
    
    return cylinder

def create_sphere(center, radius=0.03, color=[0.9, 0.6, 0.3]):
    """Create a sphere mesh at a given position."""
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
    sphere.translate(center)
    sphere.paint_uniform_color(color)
    return sphere

def create_sample_hand():
    """Create a sample hand structure for testing."""
    print("Creating sample hand model...")
    
    meshes = []
    
    # Sample hand landmarks (simplified positions)
    # Wrist
    wrist = np.array([0.5, 0.5, 0.0])
    
    # Palm sphere
    palm = create_sphere(wrist, radius=0.04, color=[0.9, 0.6, 0.3])
    meshes.append(palm)
    
    # Create 5 fingers
    finger_directions = [
        np.array([-0.15, 0.1, 0.0]),   # Thumb
        np.array([-0.05, 0.15, 0.0]),  # Index
        np.array([0.0, 0.16, 0.0]),    # Middle
        np.array([0.05, 0.15, 0.0]),   # Ring
        np.array([0.1, 0.12, 0.0]),    # Pinky
    ]
    
    colors = [
        [0.8, 0.3, 0.2],
        [0.7, 0.4, 0.2],
        [0.6, 0.5, 0.2],
        [0.7, 0.4, 0.2],
        [0.8, 0.3, 0.2],
    ]
    
    for i, (direction, color) in enumerate(zip(finger_directions, colors)):
        # Create 3 segments per finger
        for j in range(3):
            start = wrist + direction * (j / 3.0)
            end = wrist + direction * ((j + 1) / 3.0)
            
            cylinder = create_cylinder(start, end, radius=0.008, color=color)
            if cylinder:
                meshes.append(cylinder)
            
            # Add joint sphere
            joint = create_sphere(end, radius=0.01, color=[0.7, 0.3, 0.1])
            meshes.append(joint)
    
    print(f"✓ Created {len(meshes)} mesh components")
    return meshes

def test_open3d():
    """Test Open3D visualization."""
    print("=" * 60)
    print("TESTING OPEN3D 3D VISUALIZATION")
    print("=" * 60)
    print()
    
    try:
        # Create sample hand
        meshes = create_sample_hand()
        
        # Create visualizer
        print("Initializing Open3D visualizer...")
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name="Open3D Test - Sample Hand Model", width=800, height=600)
        
        print("✓ Open3D window created")
        
        # Add coordinate frame
        coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
        vis.add_geometry(coord_frame)
        
        # Add all meshes
        print(f"Adding {len(meshes)} geometries to visualizer...")
        for mesh in meshes:
            vis.add_geometry(mesh)
        
        print("✓ Geometries added")
        print()
        print("Instructions:")
        print("  - You should see a 3D hand model with:")
        print("    • Orange sphere for the palm")
        print("    • Colored cylinders for finger segments")
        print("    • Small spheres at joints")
        print("  - Use mouse to rotate, zoom, and pan")
        print("  - Close the window when done")
        print()
        print("Displaying 3D visualization...")
        
        # Run visualizer
        vis.run()
        vis.destroy_window()
        
        print()
        print("=" * 60)
        print("✓ OPEN3D TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Next step:")
        print("  Run: python hand_model.py (full integrated hand model)")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error during Open3D test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_open3d()
