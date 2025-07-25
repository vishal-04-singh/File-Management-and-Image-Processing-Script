# File Management and Image Processing Tool

A comprehensive file management application with both **GUI** and **command-line** interfaces, providing intuitive file operations, image processing, and download capabilities.

## 🚀 Features

### Core File Operations
- **Copy/Move files** with pattern matching
- **File segregation** into custom folder structures
- **Batch file renaming** with preview
- **Smart file deletion** with pattern matching
- **Directory management** (create/remove)

### Image Processing
- **Batch image resizing** with aspect ratio preservation
- **Preview functionality** before processing
- **Minimum size requirements** enforcement
- Support for multiple image formats (JPG, PNG, BMP, GIF, TIFF, WebP)

### Download Manager
- **URL-based file downloads**
- **Google Drive integration** (with gdown)
- **Batch download capabilities**
- **Progress tracking** and error handling

### User Interface Options
- **Modern GUI** with tabbed interface (tkinter-based)
- **Command-line interface** for automation/scripting
- **Cross-platform compatibility** (Windows, macOS, Linux)

## 📦 Installation

### Prerequisites
- Python 3.7+ required
- tkinter (usually included with Python)

### Install Dependencies
```bash
pip install -r requirements.txt
```

**Optional dependencies:**
- `Pillow` - for image processing
- `beautifulsoup4` + `requests` - for web downloads  
- `gdown` - for Google Drive downloads
- `pyautogui` - for Google Maps integration (CLI only)

## 🖥️ Usage

### GUI Application (Recommended)
Launch the modern graphical interface:

```bash
python3 gui_main.py
```

#### GUI Features:
- **File Operations Tab**: Copy/move files with optional segregation
- **Image Processing Tab**: Batch resize with preview
- **File Management Tab**: Rename, delete, and directory operations
- **Download Tab**: URL downloads and Google Drive integration
- **Real-time Progress**: Live feedback and error reporting

### Command Line Interface
For automation and scripting:

```bash
python3 file_manager_cli.py
```

Interactive menu with options:
- (a) Copy files
- (b) Move files  
- (c) Rename files
- (d) Resize images
- (f) Delete files
- (g) Create directories
- (h) Remove empty directories

## 📋 GUI Usage Guide

### File Operations
1. Select **Copy** or **Move** operation
2. Choose source and destination directories
3. Enter file patterns (one per line)
4. For segregation: Enable checkbox and specify folder mappings
5. Click **Execute Operation**

### Image Processing
1. Select directory containing images
2. Set minimum width/height requirements
3. Click **Preview Changes** to see what will be modified
4. Click **Resize Images** to apply changes

### File Management
1. **Rename**: Enter `old_path[TAB]new_name` pairs
2. **Delete**: Select directory and enter file patterns
3. **Directories**: Create new or remove empty directories

### Downloads
1. Set destination directory
2. Enter `URL[TAB]filename` pairs
3. Click **Download Files**

## 🔧 Technical Details

### File Structure
- `gui_main.py` - Main GUI application
- `file_operations.py` - Core file management logic
- `image_processor.py` - Image processing operations
- `download_manager.py` - Download functionality
- `file_manager_cli.py` - Original CLI script
- `requirements.txt` - Python dependencies

### Key Features
- **Threading**: Non-blocking operations prevent GUI freezing
- **Error Handling**: Comprehensive error reporting with user-friendly messages
- **Progress Tracking**: Real-time feedback for all operations
- **Input Validation**: Prevents common user errors
- **Cross-platform**: Works on Windows, macOS, and Linux

## ⚠️ Safety Features

- **Confirmation dialogs** for destructive operations
- **Preview functionality** for image resize operations
- **Detailed logging** of all operations
- **Error recovery** with partial operation completion
- **Path validation** before operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Please see the repository for license details.

## 🐛 Troubleshooting

### Common Issues
- **"tkinter not available"**: Install `python3-tk` package
- **"PIL not available"**: Install with `pip install Pillow`
- **Download errors**: Check internet connection and install `requests beautifulsoup4`

### Performance Tips
- For large file operations, use smaller batch sizes
- Image processing works best with SSD storage
- Network downloads depend on connection speed

## 📈 Changelog

### v2.0.0 - GUI Implementation
- Added modern tkinter-based GUI
- Refactored code into modular components
- Added progress tracking and error handling
- Implemented preview functionality
- Added threaded operations for better responsiveness

### v1.0.0 - Original CLI Version
- Basic file operations via command line
- Image resize functionality
- Directory management
- Download capabilities

