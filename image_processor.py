"""
Image processing operations module.
Contains image resize functionality.
"""
import os
from typing import List, Tuple, Callable, Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ImageProcessor:
    """Image processing operations."""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback
        
        if not PIL_AVAILABLE:
            self._update_progress("Warning: PIL (Pillow) not available. Image operations disabled.")
    
    def _update_progress(self, message: str):
        """Update progress if callback is provided."""
        if self.progress_callback:
            self.progress_callback(message)
    
    def is_available(self) -> bool:
        """Check if image processing is available."""
        return PIL_AVAILABLE
    
    def get_image_files(self, directory: str) -> List[str]:
        """Get all image files from directory recursively."""
        if not PIL_AVAILABLE:
            return []
            
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        image_files = []
        
        try:
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    if any(filename.lower().endswith(ext) for ext in image_extensions):
                        filepath = os.path.join(root, filename)
                        image_files.append(filepath)
        except Exception as e:
            self._update_progress(f"Error scanning directory: {str(e)}")
        
        return image_files
    
    def get_image_info(self, image_path: str) -> Optional[Tuple[int, int]]:
        """Get image dimensions."""
        if not PIL_AVAILABLE:
            return None
            
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception as e:
            self._update_progress(f"Error reading image {image_path}: {str(e)}")
            return None
    
    def resize_image(self, image_path: str, min_width: int, min_height: int) -> bool:
        """
        Resize a single image to meet minimum dimensions.
        
        Args:
            image_path: Path to the image file
            min_width: Minimum width requirement
            min_height: Minimum height requirement
            
        Returns:
            True if resize was successful or not needed, False otherwise
        """
        if not PIL_AVAILABLE:
            self._update_progress("PIL not available for image processing")
            return False
        
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Check if resize is needed
                if width >= min_width and height >= min_height:
                    self._update_progress(f"{os.path.basename(image_path)} -> ({width}, {height}) Already proper size!")
                    return True
                
                # Calculate new dimensions
                new_width, new_height = self._calculate_new_dimensions(
                    width, height, min_width, min_height
                )
                
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save resized image (replace original)
                resized_img.save(image_path)
                
                self._update_progress(f"{os.path.basename(image_path)} -> ({new_width}, {new_height}) Resized!")
                return True
                
        except Exception as e:
            self._update_progress(f"Error resizing {os.path.basename(image_path)}: {str(e)}")
            return False
    
    def _calculate_new_dimensions(self, width: int, height: int, 
                                min_width: int, min_height: int) -> Tuple[int, int]:
        """Calculate new dimensions maintaining aspect ratio."""
        if width < min_width:
            ratio = height / width
            new_width = min_width
            new_height = int(ratio * new_width)
            
            if new_height < min_height:
                # Need to adjust height too
                new_ratio = new_width / new_height
                final_height = min_height
                final_width = int(new_ratio * final_height)
                return final_width, final_height
            else:
                return new_width, new_height
                
        elif height < min_height:
            ratio = width / height
            new_height = min_height
            new_width = int(ratio * new_height)
            return new_width, new_height
        
        return width, height
    
    def resize_images_batch(self, directory: str, min_width: int, min_height: int) -> Tuple[int, int]:
        """
        Resize all images in directory to meet minimum dimensions.
        
        Args:
            directory: Directory containing images
            min_width: Minimum width requirement
            min_height: Minimum height requirement
            
        Returns:
            Tuple of (successful_resizes, total_images)
        """
        if not PIL_AVAILABLE:
            self._update_progress("PIL not available for image processing")
            return 0, 0
        
        if not os.path.exists(directory):
            raise ValueError(f"Directory does not exist: {directory}")
        
        image_files = self.get_image_files(directory)
        successful = 0
        total_images = len(image_files)
        
        self._update_progress(f"Found {total_images} image files to process")
        
        for image_path in image_files:
            if self.resize_image(image_path, min_width, min_height):
                successful += 1
        
        self._update_progress(f"Completed: {successful}/{total_images} images processed")
        return successful, total_images
    
    def preview_resize_changes(self, directory: str, min_width: int, min_height: int) -> List[dict]:
        """
        Preview what changes would be made without actually resizing.
        
        Args:
            directory: Directory containing images
            min_width: Minimum width requirement
            min_height: Minimum height requirement
            
        Returns:
            List of dictionaries with file info and proposed changes
        """
        if not PIL_AVAILABLE:
            return []
        
        if not os.path.exists(directory):
            return []
        
        image_files = self.get_image_files(directory)
        preview_data = []
        
        for image_path in image_files:
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    
                    if width >= min_width and height >= min_height:
                        action = "No change needed"
                        new_width, new_height = width, height
                    else:
                        action = "Will be resized"
                        new_width, new_height = self._calculate_new_dimensions(
                            width, height, min_width, min_height
                        )
                    
                    preview_data.append({
                        'filename': os.path.basename(image_path),
                        'path': image_path,
                        'current_size': (width, height),
                        'new_size': (new_width, new_height),
                        'action': action
                    })
                    
            except Exception as e:
                preview_data.append({
                    'filename': os.path.basename(image_path),
                    'path': image_path,
                    'current_size': None,
                    'new_size': None,
                    'action': f"Error: {str(e)}"
                })
        
        return preview_data