#!/usr/bin/env python3
"""
Launcher script for the File Management GUI application.
Provides easy startup with dependency checking.
"""

import sys
import os

def check_python_version():
    """Check if Python version is sufficient."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check for required and optional dependencies."""
    required_missing = []
    optional_missing = []
    
    # Check tkinter (required for GUI)
    try:
        import tkinter
        print("✓ tkinter available")
    except ImportError:
        required_missing.append("tkinter")
    
    # Check optional dependencies
    optional_deps = [
        ("PIL", "Pillow", "Image processing"),
        ("requests", "requests", "Web downloads"),
        ("bs4", "beautifulsoup4", "Web scraping"),
        ("gdown", "gdown", "Google Drive downloads"),
        ("pyautogui", "pyautogui", "Google Maps automation")
    ]
    
    for import_name, package_name, description in optional_deps:
        try:
            __import__(import_name)
            print(f"✓ {package_name} available - {description}")
        except ImportError:
            optional_missing.append((package_name, description))
    
    if required_missing:
        print("\n❌ Required dependencies missing:")
        for dep in required_missing:
            print(f"  - {dep}")
        if "tkinter" in required_missing:
            print("\nTo install tkinter:")
            print("  Ubuntu/Debian: sudo apt-get install python3-tk")
            print("  CentOS/RHEL: sudo yum install tkinter")
            print("  macOS: tkinter comes with Python from python.org")
            print("  Windows: tkinter comes with Python")
        return False
    
    if optional_missing:
        print("\nℹ️ Optional dependencies missing (features will be disabled):")
        for package, description in optional_missing:
            print(f"  - {package}: {description}")
        print(f"\nTo install all optional dependencies:")
        print("  pip install -r requirements.txt")
    
    return True

def launch_gui():
    """Launch the GUI application."""
    try:
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        # Import and run GUI
        from gui_main import main
        print("\n🚀 Launching File Management GUI...")
        main()
        
    except ImportError as e:
        print(f"\n❌ Error importing GUI modules: {e}")
        print("Make sure all required files are present:")
        print("  - gui_main.py")
        print("  - file_operations.py") 
        print("  - image_processor.py")
        print("  - download_manager.py")
        print("  - drag_drop.py")
        return False
    except Exception as e:
        print(f"\n❌ Error launching GUI: {e}")
        return False
    
    return True

def launch_cli():
    """Launch the CLI application."""
    try:
        print("\n🚀 Launching CLI version...")
        import subprocess
        subprocess.run([sys.executable, "file_manager_cli.py"])
    except Exception as e:
        print(f"\n❌ Error launching CLI: {e}")
        return False
    return True

def main():
    """Main launcher function."""
    print("File Management & Image Processing Tool Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    print("\nSelect interface:")
    print("1. GUI (Graphical User Interface) - Recommended")
    print("2. CLI (Command Line Interface)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == "1":
                if deps_ok:
                    if launch_gui():
                        break
                    else:
                        print("\nFalling back to CLI...")
                        launch_cli()
                        break
                else:
                    print("\n❌ Cannot launch GUI due to missing dependencies.")
                    print("Would you like to try CLI instead? (y/n)")
                    if input().lower().startswith('y'):
                        launch_cli()
                    break
                    
            elif choice == "2":
                launch_cli()
                break
                
            elif choice == "3":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()