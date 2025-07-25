"""
Drag and drop functionality for the GUI application.
Provides enhanced user experience with file dropping capabilities.
"""
import tkinter as tk
from typing import Callable, Optional


class DragDropMixin:
    """
    Mixin class to add drag and drop functionality to tkinter widgets.
    Note: This is a basic implementation. For full cross-platform support,
    consider using tkinterdnd2 package.
    """
    
    def __init__(self):
        self.drop_callback: Optional[Callable] = None
    
    def enable_drop(self, widget, callback: Callable[[str], None]):
        """
        Enable drag and drop on a widget.
        
        Args:
            widget: tkinter widget to enable drop on
            callback: Function to call when files are dropped
        """
        self.drop_callback = callback
        
        # Bind drag and drop events (basic implementation)
        widget.bind('<Button-1>', self._on_click)
        widget.bind('<B1-Motion>', self._on_drag)
        widget.bind('<ButtonRelease-1>', self._on_drop)
        
        # For better cross-platform support, you would use:
        # try:
        #     from tkinterdnd2 import DND_FILES, TkinterDnD
        #     widget.drop_target_register(DND_FILES)
        #     widget.dnd_bind('<<Drop>>', self._on_file_drop)
        # except ImportError:
        #     pass  # Fall back to basic implementation
    
    def _on_click(self, event):
        """Handle mouse click."""
        pass
    
    def _on_drag(self, event):
        """Handle mouse drag."""
        pass
    
    def _on_drop(self, event):
        """Handle mouse release (drop)."""
        pass
    
    def _on_file_drop(self, event):
        """Handle file drop event (for tkinterdnd2)."""
        if self.drop_callback:
            files = event.data.split('\n')
            for file_path in files:
                if file_path.strip():
                    self.drop_callback(file_path.strip())


def install_drag_drop_support():
    """
    Try to install enhanced drag and drop support.
    Returns True if successful, False otherwise.
    """
    try:
        import tkinterdnd2
        return True
    except ImportError:
        return False


class FileDropArea:
    """
    A specialized widget area for file dropping.
    """
    
    def __init__(self, parent, callback: Callable[[str], None], 
                 text: str = "Drop files here", height: int = 100):
        """
        Create a file drop area.
        
        Args:
            parent: Parent tkinter widget
            callback: Function to call when files are dropped
            text: Text to display in drop area
            height: Height of drop area in pixels
        """
        self.callback = callback
        
        # Create drop area frame
        self.frame = tk.Frame(parent, relief='sunken', bd=2, 
                             bg='lightgray', height=height)
        self.frame.pack(fill='x', padx=5, pady=5)
        
        # Add label
        self.label = tk.Label(self.frame, text=text, 
                             bg='lightgray', fg='darkgray',
                             font=('TkDefaultFont', 10, 'italic'))
        self.label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Enable drag and drop
        self._setup_drop_events()
    
    def _setup_drop_events(self):
        """Setup drag and drop events."""
        # Basic implementation - bind to mouse events
        self.frame.bind('<Button-1>', self._on_click)
        self.label.bind('<Button-1>', self._on_click)
        
        # Configure visual feedback
        self.frame.bind('<Enter>', self._on_enter)
        self.frame.bind('<Leave>', self._on_leave)
        
        # For enhanced support with tkinterdnd2:
        if install_drag_drop_support():
            try:
                from tkinterdnd2 import DND_FILES
                self.frame.drop_target_register(DND_FILES)
                self.frame.dnd_bind('<<Drop>>', self._on_file_drop)
                self.label.drop_target_register(DND_FILES) 
                self.label.dnd_bind('<<Drop>>', self._on_file_drop)
                
                # Update label text to indicate drop support
                self.label.config(text="Drop files here or click to browse")
            except ImportError:
                pass
    
    def _on_click(self, event):
        """Handle click - open file dialog."""
        from tkinter import filedialog
        
        # Allow multiple file selection
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[
                ("All files", "*.*"),
                ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("Text files", "*.txt *.log"),
                ("Archive files", "*.zip *.rar *.7z")
            ]
        )
        
        for file_path in files:
            if file_path:
                self.callback(file_path)
    
    def _on_enter(self, event):
        """Handle mouse enter - visual feedback."""
        self.frame.config(bg='lightblue')
        self.label.config(bg='lightblue')
    
    def _on_leave(self, event):
        """Handle mouse leave - restore appearance."""
        self.frame.config(bg='lightgray')
        self.label.config(bg='lightgray')
    
    def _on_file_drop(self, event):
        """Handle file drop event."""
        files = self.tk.splitlist(event.data)
        for file_path in files:
            if file_path:
                self.callback(file_path)
        
        # Visual feedback
        self.frame.config(bg='lightgreen')
        self.label.config(bg='lightgreen')
        self.frame.after(500, self._restore_color)
    
    def _restore_color(self):
        """Restore normal colors after drop."""
        self.frame.config(bg='lightgray')
        self.label.config(bg='lightgray')
    
    def update_text(self, text: str):
        """Update the display text."""
        self.label.config(text=text)


def create_enhanced_file_dialog(parent, title: str = "Select Files", 
                               multiple: bool = True, filetypes: list = None):
    """
    Create an enhanced file dialog with drag and drop preview.
    
    Args:
        parent: Parent widget
        title: Dialog title
        multiple: Allow multiple file selection
        filetypes: List of (description, pattern) tuples
        
    Returns:
        List of selected file paths
    """
    if filetypes is None:
        filetypes = [
            ("All files", "*.*"),
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("Text files", "*.txt *.log"),
        ]
    
    # Create dialog window
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("400x300")
    dialog.transient(parent)
    dialog.grab_set()
    
    selected_files = []
    
    def on_file_dropped(file_path):
        """Handle file drop in dialog."""
        selected_files.append(file_path)
        update_file_list()
    
    def update_file_list():
        """Update the file list display."""
        file_listbox.delete(0, tk.END)
        for file_path in selected_files:
            file_listbox.insert(tk.END, file_path)
    
    def browse_files():
        """Open standard file dialog."""
        from tkinter import filedialog
        
        if multiple:
            files = filedialog.askopenfilenames(
                title=title,
                filetypes=filetypes
            )
            selected_files.extend(files)
        else:
            file_path = filedialog.askopenfilename(
                title=title,
                filetypes=filetypes
            )
            if file_path:
                selected_files.append(file_path)
        
        update_file_list()
    
    def clear_files():
        """Clear selected files."""
        selected_files.clear()
        update_file_list()
    
    def confirm_selection():
        """Confirm and close dialog."""
        dialog.destroy()
    
    # Create drop area
    drop_area = FileDropArea(dialog, on_file_dropped, 
                            text="Drop files here or click Browse")
    
    # File list
    list_frame = tk.Frame(dialog)
    list_frame.pack(fill='both', expand=True, padx=10, pady=5)
    
    tk.Label(list_frame, text="Selected Files:").pack(anchor='w')
    
    file_listbox = tk.Listbox(list_frame)
    scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=file_listbox.yview)
    file_listbox.configure(yscrollcommand=scrollbar.set)
    
    file_listbox.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Buttons
    button_frame = tk.Frame(dialog)
    button_frame.pack(fill='x', padx=10, pady=10)
    
    tk.Button(button_frame, text="Browse", command=browse_files).pack(side='left', padx=5)
    tk.Button(button_frame, text="Clear", command=clear_files).pack(side='left', padx=5)
    tk.Button(button_frame, text="OK", command=confirm_selection).pack(side='right', padx=5)
    tk.Button(button_frame, text="Cancel", 
             command=dialog.destroy).pack(side='right', padx=5)
    
    # Wait for dialog to close
    parent.wait_window(dialog)
    
    return selected_files