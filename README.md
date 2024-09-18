# File Management and Utility Script

This Python script provides various file management and utility functions, including copying, moving, renaming, resizing images, and more.

## Features

- Copy or move files
- Copy or move files with segregation
- Rename files
- Resize images
- Delete files
- Create directories
- Remove empty directories
- (Commented out features: Download files, Get Google Maps image links)

## Dependencies

This script requires the following Python modules:

- os (built-in)
- shutil (built-in)
- PIL (Python Imaging Library)
- BeautifulSoup4
- urllib (built-in)
- gdown
- pyautogui
- threading (built-in)

You can install the required third-party dependencies using pip:

```
pip install Pillow beautifulsoup4 gdown pyautogui
```

## Usage

1. Ensure all dependencies are installed.
2. Run the script using Python:

```
python script_name.py
```

3. Follow the interactive prompts to choose and execute desired operations.

## Functions

- `copyORmove()`: Copy or move files based on user input.
- `copyORmoveANDsegregate()`: Copy or move files with custom folder segregation.
- `rename()`: Rename files based on user input.
- `resize()`: Resize images to meet minimum width and height requirements.
- `delete_files()`: Delete specified files from a given directory.
- `Mkdir()`: Create new directories based on user input.
- `Rmdir()`: Remove empty directories recursively.
- `asking_query()`: Main function to handle user interaction and function calls.

(Commented out functions: `download()`, `maps()`)

## Note

- The script operates interactively, prompting the user for inputs such as file names, paths, and operations to perform.
- Some features (download and Google Maps image links) are currently commented out in the main execution flow.
- Use caution with functions like `delete_files()` and `Rmdir()` as they can permanently remove data.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your proposed changes.

