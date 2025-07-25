"""
Download manager module.
Handles file downloads from URLs and Google Drive.
"""
import os
import urllib.request
from typing import List, Tuple, Callable, Optional

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False

try:
    import gdown
    GDOWN_AVAILABLE = True
except ImportError:
    GDOWN_AVAILABLE = False


class DownloadManager:
    """File download operations."""
    
    def __init__(self, progress_callback: Optional[Callable] = None):
        """Initialize with optional progress callback."""
        self.progress_callback = progress_callback
        
        missing_deps = []
        if not REQUESTS_AVAILABLE:
            missing_deps.append("requests")
        if not BEAUTIFULSOUP_AVAILABLE:
            missing_deps.append("beautifulsoup4")
        if not GDOWN_AVAILABLE:
            missing_deps.append("gdown")
            
        if missing_deps:
            self._update_progress(f"Warning: Missing dependencies: {', '.join(missing_deps)}")
    
    def _update_progress(self, message: str):
        """Update progress if callback is provided."""
        if self.progress_callback:
            self.progress_callback(message)
    
    def is_available(self) -> bool:
        """Check if download functionality is available."""
        return REQUESTS_AVAILABLE and BEAUTIFULSOUP_AVAILABLE
    
    def is_google_drive_available(self) -> bool:
        """Check if Google Drive download is available."""
        return GDOWN_AVAILABLE
    
    def download_file(self, url: str, filename: str, destination: str) -> bool:
        """
        Download a single file from URL.
        
        Args:
            url: URL to download from
            filename: Filename to save as
            destination: Destination directory
            
        Returns:
            True if download successful, False otherwise
        """
        if not os.path.exists(destination):
            os.makedirs(destination, exist_ok=True)
        
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Ensure filename has extension
        if not any(filename.endswith(ext) for ext in ['.jpg', '.png', '.jpeg', '.pdf', '.txt', '.zip']):
            filename += '.jpg'
        
        file_path = os.path.join(destination, filename)
        
        try:
            if "drive.google.com" in url:
                return self._download_google_drive(url, file_path, filename)
            elif any(ext in url for ext in ['.jpg', '.png', '.jpeg', '.webp']) or "duckduckgo" in url or "flickr" not in url:
                return self._download_direct(url, file_path, filename)
            else:
                return self._download_from_page(url, file_path, filename)
                
        except Exception as e:
            self._update_progress(f"Error downloading {filename}: {str(e)}")
            return False
    
    def _download_google_drive(self, url: str, file_path: str, filename: str) -> bool:
        """Download from Google Drive."""
        if not GDOWN_AVAILABLE:
            self._update_progress(f"gdown not available for Google Drive download: {filename}")
            return False
        
        try:
            # Extract file ID from Google Drive URL
            file_id = url.split('/')[5] if '/d/' in url else url.split('/')[-2]
            download_url = f'https://drive.google.com/uc?id={file_id}'
            
            gdown.download(download_url, file_path, quiet=False)
            self._update_progress(f"Downloaded from Google Drive: {filename}")
            return True
            
        except Exception as e:
            self._update_progress(f"Error downloading from Google Drive {filename}: {str(e)}")
            return False
    
    def _download_direct(self, url: str, file_path: str, filename: str) -> bool:
        """Download directly from URL."""
        try:
            urllib.request.urlretrieve(url, file_path)
            self._update_progress(f"Downloaded: {filename}")
            return True
            
        except Exception as e:
            self._update_progress(f"Error downloading {filename}: {str(e)}")
            return False
    
    def _download_from_page(self, url: str, file_path: str, filename: str) -> bool:
        """Download by extracting image URL from webpage."""
        if not (REQUESTS_AVAILABLE and BEAUTIFULSOUP_AVAILABLE):
            self._update_progress(f"requests/beautifulsoup not available: {filename}")
            return False
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            
            image_url = None
            for image in images:
                src = image.get('src', '')
                if '.jpg' in src:
                    if not src.startswith('http'):
                        image_url = 'https:' + src
                    else:
                        image_url = src
                    break
            
            if image_url:
                urllib.request.urlretrieve(image_url, file_path)
                self._update_progress(f"Downloaded from page: {filename}")
                return True
            else:
                self._update_progress(f"No suitable image found on page: {filename}")
                return False
                
        except Exception as e:
            self._update_progress(f"Error downloading from page {filename}: {str(e)}")
            return False
    
    def download_files_batch(self, url_filename_pairs: List[Tuple[str, str]], destination: str) -> Tuple[int, int]:
        """
        Download multiple files.
        
        Args:
            url_filename_pairs: List of (url, filename) tuples
            destination: Destination directory
            
        Returns:
            Tuple of (successful_downloads, total_files)
        """
        successful = 0
        total_files = len(url_filename_pairs)
        
        for url, filename in url_filename_pairs:
            if self.download_file(url, filename, destination):
                successful += 1
        
        self._update_progress(f"Download completed: {successful}/{total_files} files")
        return successful, total_files
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if URL is accessible.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is accessible, False otherwise
        """
        if not REQUESTS_AVAILABLE:
            return True  # Can't validate without requests, assume valid
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = requests.head(url, timeout=10)
            return response.status_code == 200
            
        except Exception:
            return False
    
    def get_file_size(self, url: str) -> Optional[int]:
        """
        Get file size from URL.
        
        Args:
            url: URL to check
            
        Returns:
            File size in bytes, or None if unavailable
        """
        if not REQUESTS_AVAILABLE:
            return None
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = requests.head(url, timeout=10)
            content_length = response.headers.get('content-length')
            
            if content_length:
                return int(content_length)
            else:
                return None
                
        except Exception:
            return None