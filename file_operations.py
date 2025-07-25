"""
Core file management operations module.
Contains the business logic for file operations without UI dependencies.
"""
import os
import shutil
import threading
from typing import List, Tuple, Callable, Optional


class FileOperations:
    """Core file management operations."""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback
        
    def _update_progress(self, message: str):
        """Update progress if callback is provided."""
        if self.progress_callback:
            self.progress_callback(message)
    
    def get_all_files(self, source_path: str) -> List[str]:
        """Get all file paths from source directory recursively."""
        file_paths = []
        try:
            for root, dirs, files in os.walk(source_path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)
        except Exception as e:
            self._update_progress(f"Error scanning directory: {str(e)}")
        return file_paths
    
    def copy_or_move_files(self, file_patterns: List[str], source_path: str, 
                          destination_path: str, operation: str = 'copy') -> Tuple[int, int]:
        """
        Copy or move files matching patterns.
        
        Args:
            file_patterns: List of file patterns to match
            source_path: Source directory path
            destination_path: Destination directory path
            operation: 'copy' or 'move'
            
        Returns:
            Tuple of (successful_operations, total_files)
        """
        if not os.path.exists(source_path):
            raise ValueError(f"Source path does not exist: {source_path}")
        
        if not os.path.exists(destination_path):
            os.makedirs(destination_path, exist_ok=True)
        
        all_files = self.get_all_files(source_path)
        successful = 0
        total_files = len(file_patterns)
        
        for pattern in file_patterns:
            pattern = pattern.strip()
            if not pattern.endswith('.'):
                pattern += '.'
                
            found = False
            for file_path in all_files:
                filename = os.path.basename(file_path)
                if filename.startswith(pattern):
                    try:
                        if operation == 'copy':
                            shutil.copy(file_path, destination_path)
                        else:
                            shutil.move(file_path, destination_path)
                        self._update_progress(f"{operation.capitalize()}d: {filename}")
                        successful += 1
                        found = True
                        break
                    except Exception as e:
                        self._update_progress(f"Error {operation}ing {filename}: {str(e)}")
            
            if not found:
                self._update_progress(f"File not found: {pattern}")
        
        return successful, total_files
    
    def copy_or_move_with_segregation(self, files_and_folders: List[Tuple[str, str]], 
                                    source_path: str, destination_path: str, 
                                    operation: str = 'copy') -> Tuple[int, int]:
        """
        Copy or move files with folder segregation.
        
        Args:
            files_and_folders: List of (file_pattern, folder_path) tuples
            source_path: Source directory path
            destination_path: Base destination directory path
            operation: 'copy' or 'move'
            
        Returns:
            Tuple of (successful_operations, total_files)
        """
        if not os.path.exists(source_path):
            raise ValueError(f"Source path does not exist: {source_path}")
        
        # Create destination folders
        for _, folder_path in files_and_folders:
            full_dest_path = os.path.join(destination_path, folder_path)
            os.makedirs(full_dest_path, exist_ok=True)
        
        all_files = self.get_all_files(source_path)
        successful = 0
        total_files = len(files_and_folders)
        
        for file_pattern, folder_path in files_and_folders:
            file_pattern = file_pattern.strip()
            if not file_pattern.endswith('.'):
                file_pattern += '.'
                
            found = False
            for file_path in all_files:
                filename = os.path.basename(file_path)
                if filename.startswith(file_pattern):
                    try:
                        dest_folder = os.path.join(destination_path, folder_path)
                        if operation == 'copy':
                            shutil.copy(file_path, dest_folder)
                        else:
                            shutil.move(file_path, dest_folder)
                        self._update_progress(f"{operation.capitalize()}d {filename} to {folder_path}")
                        successful += 1
                        found = True
                        break
                    except Exception as e:
                        self._update_progress(f"Error {operation}ing {filename}: {str(e)}")
            
            if not found:
                self._update_progress(f"File not found: {file_pattern}")
        
        return successful, total_files
    
    def rename_files(self, rename_pairs: List[Tuple[str, str]]) -> Tuple[int, int]:
        """
        Rename files based on old_path, new_name pairs.
        
        Args:
            rename_pairs: List of (old_path, new_name) tuples
            
        Returns:
            Tuple of (successful_renames, total_files)
        """
        successful = 0
        total_files = len(rename_pairs)
        
        for old_path, new_name in rename_pairs:
            try:
                old_path = old_path.strip()
                new_name = new_name.strip()
                
                # Ensure file has extension
                if not any(new_name.endswith(ext) for ext in ['.jpg', '.png', '.pdf', '.jpeg']):
                    new_name += '.jpg'
                
                # Get directory path and create new full path
                directory = os.path.dirname(old_path)
                new_path = os.path.join(directory, new_name)
                
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    self._update_progress(f"Renamed: {os.path.basename(old_path)} -> {new_name}")
                    successful += 1
                else:
                    self._update_progress(f"File not found: {old_path}")
                    
            except Exception as e:
                self._update_progress(f"Error renaming {old_path}: {str(e)}")
        
        return successful, total_files
    
    def delete_files(self, file_patterns: List[str], source_path: str) -> Tuple[int, int]:
        """
        Delete files matching patterns.
        
        Args:
            file_patterns: List of file patterns to match
            source_path: Source directory path
            
        Returns:
            Tuple of (successful_deletions, total_patterns)
        """
        if not os.path.exists(source_path):
            raise ValueError(f"Source path does not exist: {source_path}")
        
        all_files = self.get_all_files(source_path)
        successful = 0
        total_patterns = len(file_patterns)
        
        for pattern in file_patterns:
            pattern = pattern.strip()
            if not pattern.endswith('.'):
                pattern += '.'
                
            found = False
            for file_path in all_files:
                filename = os.path.basename(file_path)
                if filename.lower().startswith(pattern.lower()):
                    try:
                        os.remove(file_path)
                        self._update_progress(f"Deleted: {filename}")
                        successful += 1
                        found = True
                        break
                    except Exception as e:
                        self._update_progress(f"Error deleting {filename}: {str(e)}")
            
            if not found:
                self._update_progress(f"File not found: {pattern}")
        
        return successful, total_patterns
    
    def create_directories(self, dir_paths: List[str], base_path: str) -> Tuple[int, int]:
        """
        Create directories.
        
        Args:
            dir_paths: List of directory paths to create
            base_path: Base directory path
            
        Returns:
            Tuple of (successful_creations, total_directories)
        """
        successful = 0
        total_dirs = len(dir_paths)
        
        for dir_path in dir_paths:
            try:
                dir_path = dir_path.strip()
                # Handle nested directories
                folders = dir_path.split(os.sep)
                current_path = base_path
                
                for folder in folders:
                    if folder:  # Skip empty strings
                        current_path = os.path.join(current_path, folder)
                        os.makedirs(current_path, exist_ok=True)
                
                self._update_progress(f"Created directory: {dir_path}")
                successful += 1
                
            except Exception as e:
                self._update_progress(f"Error creating directory {dir_path}: {str(e)}")
        
        return successful, total_dirs
    
    def remove_empty_directories(self, source_path: str) -> int:
        """
        Remove empty directories recursively.
        
        Args:
            source_path: Source directory path
            
        Returns:
            Number of directories removed
        """
        if not os.path.exists(source_path):
            raise ValueError(f"Source path does not exist: {source_path}")
        
        removed_count = 0
        # Try multiple passes to handle nested empty directories
        for _ in range(20):
            for root, dirs, files in os.walk(source_path, topdown=False):
                for directory in dirs:
                    dir_path = os.path.join(root, directory)
                    try:
                        os.rmdir(dir_path)
                        self._update_progress(f"Removed empty directory: {dir_path}")
                        removed_count += 1
                    except OSError:
                        # Directory not empty or other error
                        pass
        
        return removed_count