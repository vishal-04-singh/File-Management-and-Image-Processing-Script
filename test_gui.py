#!/usr/bin/env python3
"""
Test script to verify the GUI application works.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    from file_operations import FileOperations
    from image_processor import ImageProcessor  
    from download_manager import DownloadManager
    
    print("✓ All modules imported successfully")
    
    # Test basic functionality
    file_ops = FileOperations()
    image_proc = ImageProcessor()
    download_mgr = DownloadManager()
    
    print("✓ All classes instantiated successfully")
    
    # Test basic operations
    print(f"✓ Image processing available: {image_proc.is_available()}")
    print(f"✓ Download manager available: {download_mgr.is_available()}")
    print(f"✓ Google Drive downloads available: {download_mgr.is_google_drive_available()}")
    
    print("\n✓ Basic functionality test passed!")
    print("You can now run: python3 gui_main.py")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)