"""
GUI File Management Application
Modern tkinter-based interface for file management operations.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from typing import Optional, List, Tuple

# Try importing our modules
try:
    from file_operations import FileOperations
    from image_processor import ImageProcessor
    from download_manager import DownloadManager
except ImportError as e:
    messagebox.showerror("Import Error", f"Failed to import modules: {e}")
    exit(1)


class FileManagerGUI:
    """Main GUI application for file management."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Management & Image Processing Tool")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Initialize business logic classes
        self.file_ops = FileOperations(progress_callback=self.update_progress)
        self.image_processor = ImageProcessor(progress_callback=self.update_progress)
        self.download_manager = DownloadManager(progress_callback=self.update_progress)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_file_operations_tab()
        self.create_image_processing_tab()
        self.create_file_management_tab()
        self.create_download_tab()
        
        # Create progress area
        self.create_progress_area()
        
    def create_file_operations_tab(self):
        """Create the file operations tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="File Operations")
        
        # Main container with scrollbar
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Operation type selection
        op_frame = ttk.LabelFrame(scrollable_frame, text="Operation Type", padding=10)
        op_frame.pack(fill='x', padx=5, pady=5)
        
        self.operation_var = tk.StringVar(value="copy")
        ttk.Radiobutton(op_frame, text="Copy Files", variable=self.operation_var, 
                       value="copy").pack(side='left', padx=10)
        ttk.Radiobutton(op_frame, text="Move Files", variable=self.operation_var, 
                       value="move").pack(side='left', padx=10)
        
        # Segregation option
        seg_frame = ttk.LabelFrame(scrollable_frame, text="Segregation", padding=10)
        seg_frame.pack(fill='x', padx=5, pady=5)
        
        self.segregation_var = tk.BooleanVar()
        ttk.Checkbutton(seg_frame, text="Enable folder segregation", 
                       variable=self.segregation_var,
                       command=self.toggle_segregation).pack(anchor='w')
        
        # Source and destination paths
        path_frame = ttk.LabelFrame(scrollable_frame, text="Paths", padding=10)
        path_frame.pack(fill='x', padx=5, pady=5)
        
        # Source path
        ttk.Label(path_frame, text="Source Directory:").grid(row=0, column=0, sticky='w', pady=2)
        self.source_var = tk.StringVar()
        source_entry = ttk.Entry(path_frame, textvariable=self.source_var, width=50)
        source_entry.grid(row=0, column=1, padx=(5, 5), pady=2, sticky='ew')
        ttk.Button(path_frame, text="Browse", 
                  command=lambda: self.browse_directory(self.source_var)).grid(row=0, column=2, padx=5, pady=2)
        
        # Destination path
        ttk.Label(path_frame, text="Destination Directory:").grid(row=1, column=0, sticky='w', pady=2)
        self.dest_var = tk.StringVar()
        dest_entry = ttk.Entry(path_frame, textvariable=self.dest_var, width=50)
        dest_entry.grid(row=1, column=1, padx=(5, 5), pady=2, sticky='ew')
        ttk.Button(path_frame, text="Browse", 
                  command=lambda: self.browse_directory(self.dest_var)).grid(row=1, column=2, padx=5, pady=2)
        
        path_frame.columnconfigure(1, weight=1)
        
        # File patterns
        pattern_frame = ttk.LabelFrame(scrollable_frame, text="File Patterns", padding=10)
        pattern_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(pattern_frame, text="Enter file patterns (one per line):").pack(anchor='w')
        self.pattern_text = scrolledtext.ScrolledText(pattern_frame, height=6, width=50)
        self.pattern_text.pack(fill='both', expand=True, pady=5)
        
        # Segregation frame (initially hidden)
        self.seg_config_frame = ttk.LabelFrame(scrollable_frame, text="Segregation Configuration", padding=10)
        
        ttk.Label(self.seg_config_frame, text="Enter: filename[TAB]folder_path (one per line):").pack(anchor='w')
        self.seg_text = scrolledtext.ScrolledText(self.seg_config_frame, height=6, width=50)
        self.seg_text.pack(fill='both', expand=True, pady=5)
        
        # Execute button
        execute_frame = ttk.Frame(scrollable_frame)
        execute_frame.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(execute_frame, text="Execute Operation", 
                  command=self.execute_file_operation).pack(pady=5)
        
        # Pack scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_image_processing_tab(self):
        """Create the image processing tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Image Processing")
        
        # Check if PIL is available
        if not self.image_processor.is_available():
            ttk.Label(frame, text="PIL (Pillow) not available. Image processing disabled.",
                     foreground="red").pack(pady=20)
            return
        
        # Directory selection
        dir_frame = ttk.LabelFrame(frame, text="Target Directory", padding=10)
        dir_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(dir_frame, text="Directory containing images:").grid(row=0, column=0, sticky='w', pady=5)
        self.image_dir_var = tk.StringVar()
        image_dir_entry = ttk.Entry(dir_frame, textvariable=self.image_dir_var, width=50)
        image_dir_entry.grid(row=0, column=1, padx=(5, 5), pady=5, sticky='ew')
        ttk.Button(dir_frame, text="Browse", 
                  command=lambda: self.browse_directory(self.image_dir_var)).grid(row=0, column=2, padx=5, pady=5)
        
        dir_frame.columnconfigure(1, weight=1)
        
        # Size settings
        size_frame = ttk.LabelFrame(frame, text="Minimum Size Requirements", padding=10)
        size_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(size_frame, text="Minimum Width:").grid(row=0, column=0, sticky='w', pady=5)
        self.min_width_var = tk.StringVar(value="800")
        ttk.Entry(size_frame, textvariable=self.min_width_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(size_frame, text="Minimum Height:").grid(row=0, column=2, sticky='w', padx=(20, 5), pady=5)
        self.min_height_var = tk.StringVar(value="600")
        ttk.Entry(size_frame, textvariable=self.min_height_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # Preview area
        preview_frame = ttk.LabelFrame(frame, text="Preview", padding=10)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.preview_tree = ttk.Treeview(preview_frame, columns=('current', 'new', 'action'), show='tree headings')
        self.preview_tree.heading('#0', text='Filename')
        self.preview_tree.heading('current', text='Current Size')
        self.preview_tree.heading('new', text='New Size')
        self.preview_tree.heading('action', text='Action')
        
        preview_scroll = ttk.Scrollbar(preview_frame, orient='vertical', command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=preview_scroll.set)
        
        self.preview_tree.pack(side='left', fill='both', expand=True)
        preview_scroll.pack(side='right', fill='y')
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Preview Changes", 
                  command=self.preview_resize).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Resize Images", 
                  command=self.execute_resize).pack(side='left', padx=5)
        
    def create_file_management_tab(self):
        """Create the file management tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="File Management")
        
        # Create sub-notebook for different operations
        sub_notebook = ttk.Notebook(frame)
        sub_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Rename tab
        self.create_rename_tab(sub_notebook)
        
        # Delete tab
        self.create_delete_tab(sub_notebook)
        
        # Directory operations tab
        self.create_directory_tab(sub_notebook)
        
    def create_rename_tab(self, parent):
        """Create the rename files sub-tab."""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Rename Files")
        
        # Instructions
        ttk.Label(frame, text="Enter old_path[TAB]new_name pairs (one per line):",
                 font=('TkDefaultFont', 9, 'italic')).pack(anchor='w', padx=10, pady=5)
        
        # Text area for rename pairs
        self.rename_text = scrolledtext.ScrolledText(frame, height=15, width=70)
        self.rename_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Button
        ttk.Button(frame, text="Rename Files", 
                  command=self.execute_rename).pack(pady=10)
        
    def create_delete_tab(self, parent):
        """Create the delete files sub-tab."""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Delete Files")
        
        # Source directory
        dir_frame = ttk.LabelFrame(frame, text="Source Directory", padding=10)
        dir_frame.pack(fill='x', padx=10, pady=10)
        
        self.delete_source_var = tk.StringVar()
        delete_entry = ttk.Entry(dir_frame, textvariable=self.delete_source_var, width=50)
        delete_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ttk.Button(dir_frame, text="Browse", 
                  command=lambda: self.browse_directory(self.delete_source_var)).pack(side='right')
        
        # File patterns
        pattern_frame = ttk.LabelFrame(frame, text="File Patterns to Delete", padding=10)
        pattern_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(pattern_frame, text="Enter file patterns (one per line):",
                 font=('TkDefaultFont', 9, 'italic')).pack(anchor='w')
        self.delete_pattern_text = scrolledtext.ScrolledText(pattern_frame, height=10, width=50)
        self.delete_pattern_text.pack(fill='both', expand=True, pady=5)
        
        # Warning and button
        ttk.Label(frame, text="⚠️ Warning: This action cannot be undone!",
                 foreground="red", font=('TkDefaultFont', 10, 'bold')).pack(pady=5)
        ttk.Button(frame, text="Delete Files", 
                  command=self.execute_delete).pack(pady=10)
        
    def create_directory_tab(self, parent):
        """Create the directory operations sub-tab."""
        frame = ttk.Frame(parent)
        parent.add(frame, text="Directories")
        
        # Create directories section
        create_frame = ttk.LabelFrame(frame, text="Create Directories", padding=10)
        create_frame.pack(fill='x', padx=10, pady=10)
        
        # Base path for creation
        ttk.Label(create_frame, text="Base Directory:").grid(row=0, column=0, sticky='w', pady=2)
        self.mkdir_base_var = tk.StringVar()
        mkdir_entry = ttk.Entry(create_frame, textvariable=self.mkdir_base_var, width=40)
        mkdir_entry.grid(row=0, column=1, padx=(5, 5), pady=2, sticky='ew')
        ttk.Button(create_frame, text="Browse", 
                  command=lambda: self.browse_directory(self.mkdir_base_var)).grid(row=0, column=2, padx=5, pady=2)
        
        create_frame.columnconfigure(1, weight=1)
        
        # Directory paths to create
        ttk.Label(create_frame, text="Directory paths to create (one per line):").grid(row=1, column=0, columnspan=3, 
                                                                                      sticky='w', pady=(10, 2))
        self.mkdir_text = scrolledtext.ScrolledText(create_frame, height=6, width=50)
        self.mkdir_text.grid(row=2, column=0, columnspan=3, sticky='ew', pady=5)
        
        ttk.Button(create_frame, text="Create Directories", 
                  command=self.execute_mkdir).grid(row=3, column=1, pady=10)
        
        # Remove empty directories section
        remove_frame = ttk.LabelFrame(frame, text="Remove Empty Directories", padding=10)
        remove_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(remove_frame, text="Source Directory:").grid(row=0, column=0, sticky='w', pady=2)
        self.rmdir_source_var = tk.StringVar()
        rmdir_entry = ttk.Entry(remove_frame, textvariable=self.rmdir_source_var, width=40)
        rmdir_entry.grid(row=0, column=1, padx=(5, 5), pady=2, sticky='ew')
        ttk.Button(remove_frame, text="Browse", 
                  command=lambda: self.browse_directory(self.rmdir_source_var)).grid(row=0, column=2, padx=5, pady=2)
        
        remove_frame.columnconfigure(1, weight=1)
        
        ttk.Button(remove_frame, text="Remove Empty Directories", 
                  command=self.execute_rmdir).grid(row=1, column=1, pady=10)
        
    def create_download_tab(self):
        """Create the download tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Downloads")
        
        # Check if download functionality is available
        if not self.download_manager.is_available():
            ttk.Label(frame, text="Download functionality requires 'requests' and 'beautifulsoup4' packages.",
                     foreground="red").pack(pady=20)
        
        # Destination directory
        dest_frame = ttk.LabelFrame(frame, text="Destination Directory", padding=10)
        dest_frame.pack(fill='x', padx=10, pady=10)
        
        self.download_dest_var = tk.StringVar()
        download_entry = ttk.Entry(dest_frame, textvariable=self.download_dest_var, width=50)
        download_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ttk.Button(dest_frame, text="Browse", 
                  command=lambda: self.browse_directory(self.download_dest_var)).pack(side='right')
        
        # URL and filename pairs
        url_frame = ttk.LabelFrame(frame, text="Downloads", padding=10)
        url_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(url_frame, text="Enter URL[TAB]filename pairs (one per line):",
                 font=('TkDefaultFont', 9, 'italic')).pack(anchor='w')
        self.download_text = scrolledtext.ScrolledText(url_frame, height=12, width=70)
        self.download_text.pack(fill='both', expand=True, pady=5)
        
        # Google Drive notice
        if self.download_manager.is_google_drive_available():
            ttk.Label(url_frame, text="✓ Google Drive downloads supported",
                     foreground="green").pack(anchor='w', pady=2)
        else:
            ttk.Label(url_frame, text="⚠️ Google Drive downloads require 'gdown' package",
                     foreground="orange").pack(anchor='w', pady=2)
        
        # Button
        ttk.Button(frame, text="Download Files", 
                  command=self.execute_download).pack(pady=10)
        
    def create_progress_area(self):
        """Create the progress and log area."""
        # Progress frame at bottom
        progress_frame = ttk.LabelFrame(self.root, text="Progress & Logs", padding=5)
        progress_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Progress text area
        self.progress_text = scrolledtext.ScrolledText(progress_frame, height=8, width=80,
                                                      state='disabled')
        self.progress_text.pack(fill='both', expand=True)
        
        # Clear button
        ttk.Button(progress_frame, text="Clear Log", 
                  command=self.clear_progress).pack(anchor='e', pady=(5, 0))
        
    # Event handlers and utility methods
    
    def browse_directory(self, var):
        """Browse for directory and set variable."""
        directory = filedialog.askdirectory()
        if directory:
            var.set(directory)
    
    def toggle_segregation(self):
        """Toggle segregation configuration visibility."""
        if self.segregation_var.get():
            self.seg_config_frame.pack(fill='both', expand=True, padx=5, pady=5)
        else:
            self.seg_config_frame.pack_forget()
    
    def update_progress(self, message: str):
        """Update progress text area."""
        self.progress_text.config(state='normal')
        self.progress_text.insert('end', f"{message}\n")
        self.progress_text.see('end')
        self.progress_text.config(state='disabled')
        self.root.update()
    
    def clear_progress(self):
        """Clear progress text area."""
        self.progress_text.config(state='normal')
        self.progress_text.delete(1.0, 'end')
        self.progress_text.config(state='disabled')
    
    def run_in_thread(self, func):
        """Run function in separate thread to prevent GUI freezing."""
        thread = threading.Thread(target=func, daemon=True)
        thread.start()
    
    # Operation executors
    
    def execute_file_operation(self):
        """Execute file copy/move operation."""
        def operation():
            try:
                source = self.source_var.get().strip()
                dest = self.dest_var.get().strip()
                operation_type = self.operation_var.get()
                
                if not source or not dest:
                    messagebox.showerror("Error", "Please select source and destination directories")
                    return
                
                if self.segregation_var.get():
                    # Parse segregation data
                    seg_data = []
                    for line in self.seg_text.get("1.0", "end-1c").strip().split('\n'):
                        if line.strip():
                            parts = line.split('\t')
                            if len(parts) >= 2:
                                seg_data.append((parts[0].strip(), parts[1].strip()))
                    
                    if not seg_data:
                        messagebox.showerror("Error", "Please enter segregation configuration")
                        return
                    
                    successful, total = self.file_ops.copy_or_move_with_segregation(
                        seg_data, source, dest, operation_type
                    )
                else:
                    # Parse file patterns
                    patterns = []
                    for line in self.pattern_text.get("1.0", "end-1c").strip().split('\n'):
                        if line.strip():
                            patterns.append(line.strip())
                    
                    if not patterns:
                        messagebox.showerror("Error", "Please enter file patterns")
                        return
                    
                    successful, total = self.file_ops.copy_or_move_files(
                        patterns, source, dest, operation_type
                    )
                
                messagebox.showinfo("Completed", f"Operation completed: {successful}/{total} files processed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Operation failed: {str(e)}")
        
        self.run_in_thread(operation)
    
    def preview_resize(self):
        """Preview image resize changes."""
        def preview():
            try:
                directory = self.image_dir_var.get().strip()
                min_width = int(self.min_width_var.get())
                min_height = int(self.min_height_var.get())
                
                if not directory:
                    messagebox.showerror("Error", "Please select a directory")
                    return
                
                # Clear previous preview
                for item in self.preview_tree.get_children():
                    self.preview_tree.delete(item)
                
                preview_data = self.image_processor.preview_resize_changes(directory, min_width, min_height)
                
                for item in preview_data:
                    current_size = f"{item['current_size'][0]}x{item['current_size'][1]}" if item['current_size'] else "Error"
                    new_size = f"{item['new_size'][0]}x{item['new_size'][1]}" if item['new_size'] else "N/A"
                    
                    self.preview_tree.insert('', 'end', text=item['filename'],
                                           values=(current_size, new_size, item['action']))
                
                self.update_progress(f"Preview completed: {len(preview_data)} images found")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid width and height values")
            except Exception as e:
                messagebox.showerror("Error", f"Preview failed: {str(e)}")
        
        self.run_in_thread(preview)
    
    def execute_resize(self):
        """Execute image resize operation."""
        def resize():
            try:
                directory = self.image_dir_var.get().strip()
                min_width = int(self.min_width_var.get())
                min_height = int(self.min_height_var.get())
                
                if not directory:
                    messagebox.showerror("Error", "Please select a directory")
                    return
                
                # Confirm operation
                result = messagebox.askyesno("Confirm", 
                                           "This will modify image files. Are you sure you want to continue?")
                if not result:
                    return
                
                successful, total = self.image_processor.resize_images_batch(directory, min_width, min_height)
                messagebox.showinfo("Completed", f"Resize completed: {successful}/{total} images processed")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid width and height values")
            except Exception as e:
                messagebox.showerror("Error", f"Resize failed: {str(e)}")
        
        self.run_in_thread(resize)
    
    def execute_rename(self):
        """Execute file rename operation."""
        def rename():
            try:
                rename_pairs = []
                for line in self.rename_text.get("1.0", "end-1c").strip().split('\n'):
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            rename_pairs.append((parts[0].strip(), parts[1].strip()))
                
                if not rename_pairs:
                    messagebox.showerror("Error", "Please enter rename pairs")
                    return
                
                successful, total = self.file_ops.rename_files(rename_pairs)
                messagebox.showinfo("Completed", f"Rename completed: {successful}/{total} files processed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Rename failed: {str(e)}")
        
        self.run_in_thread(rename)
    
    def execute_delete(self):
        """Execute file delete operation."""
        def delete():
            try:
                source = self.delete_source_var.get().strip()
                
                if not source:
                    messagebox.showerror("Error", "Please select source directory")
                    return
                
                patterns = []
                for line in self.delete_pattern_text.get("1.0", "end-1c").strip().split('\n'):
                    if line.strip():
                        patterns.append(line.strip())
                
                if not patterns:
                    messagebox.showerror("Error", "Please enter file patterns")
                    return
                
                # Confirm operation
                result = messagebox.askyesno("Confirm Delete", 
                                           "This will permanently delete files. Are you sure?")
                if not result:
                    return
                
                successful, total = self.file_ops.delete_files(patterns, source)
                messagebox.showinfo("Completed", f"Delete completed: {successful}/{total} patterns processed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed: {str(e)}")
        
        self.run_in_thread(delete)
    
    def execute_mkdir(self):
        """Execute directory creation."""
        def mkdir():
            try:
                base_path = self.mkdir_base_var.get().strip()
                
                if not base_path:
                    messagebox.showerror("Error", "Please select base directory")
                    return
                
                dir_paths = []
                for line in self.mkdir_text.get("1.0", "end-1c").strip().split('\n'):
                    if line.strip():
                        dir_paths.append(line.strip())
                
                if not dir_paths:
                    messagebox.showerror("Error", "Please enter directory paths")
                    return
                
                successful, total = self.file_ops.create_directories(dir_paths, base_path)
                messagebox.showinfo("Completed", f"Directory creation completed: {successful}/{total} directories processed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Directory creation failed: {str(e)}")
        
        self.run_in_thread(mkdir)
    
    def execute_rmdir(self):
        """Execute empty directory removal."""
        def rmdir():
            try:
                source = self.rmdir_source_var.get().strip()
                
                if not source:
                    messagebox.showerror("Error", "Please select source directory")
                    return
                
                # Confirm operation
                result = messagebox.askyesno("Confirm", 
                                           "This will remove empty directories. Continue?")
                if not result:
                    return
                
                removed_count = self.file_ops.remove_empty_directories(source)
                messagebox.showinfo("Completed", f"Removed {removed_count} empty directories")
                
            except Exception as e:
                messagebox.showerror("Error", f"Directory removal failed: {str(e)}")
        
        self.run_in_thread(rmdir)
    
    def execute_download(self):
        """Execute file download operation."""
        def download():
            try:
                dest = self.download_dest_var.get().strip()
                
                if not dest:
                    messagebox.showerror("Error", "Please select destination directory")
                    return
                
                url_filename_pairs = []
                for line in self.download_text.get("1.0", "end-1c").strip().split('\n'):
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            url_filename_pairs.append((parts[0].strip(), parts[1].strip()))
                
                if not url_filename_pairs:
                    messagebox.showerror("Error", "Please enter URL and filename pairs")
                    return
                
                successful, total = self.download_manager.download_files_batch(url_filename_pairs, dest)
                messagebox.showinfo("Completed", f"Download completed: {successful}/{total} files processed")
                
            except Exception as e:
                messagebox.showerror("Error", f"Download failed: {str(e)}")
        
        self.run_in_thread(download)


def main():
    """Main application entry point."""
    root = tk.Tk()
    
    # Try to set icon (optional)
    try:
        root.iconbitmap(default="icon.ico")
    except:
        pass  # Icon file not found, continue without it
    
    app = FileManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()