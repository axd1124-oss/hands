"""
Step 1: Dependency Validation Script
Run this first to ensure all dependencies are properly installed.
"""

import sys

def check_dependency(module_name, import_name=None):
    """Check if a dependency is installed and importable."""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"✓ {module_name} is installed")
        return True
    except ImportError as e:
        print(f"✗ {module_name} is NOT installed: {e}")
        return False

def get_version(module_name, import_name=None):
    """Get version of installed module."""
    if import_name is None:
        import_name = module_name
    
    try:
        mod = __import__(import_name)
        version = getattr(mod, '__version__', 'unknown')
        return version
    except:
        return 'N/A'

def main():
    """Check all required dependencies."""
    print("=" * 60)
    print("DEPENDENCY VALIDATION")
    print("=" * 60)
    print()
    
    dependencies = [
        ('mediapipe', 'mediapipe'),
        ('opencv-python', 'cv2'),
        ('open3d', 'open3d'),
        ('numpy', 'numpy'),
    ]
    
    all_installed = True
    
    for pkg_name, import_name in dependencies:
        installed = check_dependency(pkg_name, import_name)
        if installed:
            version = get_version(pkg_name, import_name)
            print(f"  Version: {version}")
        print()
        all_installed = all_installed and installed
    
    print("=" * 60)
    if all_installed:
        print("✓ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
        print()
        print("Next steps:")
        print("  1. Run: python test_mediapipe.py (test hand detection)")
        print("  2. Run: python test_open3d.py (test 3D visualization)")
        print("  3. Run: python hand_model.py (full hand model)")
    else:
        print("✗ SOME DEPENDENCIES ARE MISSING")
        print()
        print("To install all dependencies, run:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
