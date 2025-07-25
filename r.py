import os
import shutil
import urllib.request
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import threading

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File & Image Manager")
        self.root.geometry("700x500")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.selected_files = []
        self.source = ""
        self.destination = ""

        self.setup_copy_move_tab()
        self.setup_rename_tab()
        self.setup_resize_tab()
        self.setup_download_tab()
        self.setup_delete_mkdir_tab()

    # ---------- Copy/Move Tab ----------
    def setup_copy_move_tab(self):
        tab = Frame(self.notebook)
        self.notebook.add(tab, text="Copy / Move")

        self.operation = StringVar(value='copy')
        Label(tab, text="Select Operation:").pack(pady=5)
        Radiobutton(tab, text="Copy", variable=self.operation, value='copy').pack()
        Radiobutton(tab, text="Move", variable=self.operation, value='move').pack()

        Button(tab, text="Select Files", command=self.select_files).pack(pady=5)
        self.file_listbox = Listbox(tab, height=5)
        self.file_listbox.pack(pady=5, fill='x')

        Button(tab, text="Select Destination Folder", command=self.select_destination).pack(pady=5)
        self.dst_label = Label(tab, text="Destination: Not selected")
        self.dst_label.pack()

        Button(tab, text="Start Operation", command=self.start_copy_move).pack(pady=10)

    def select_files(self):
        self.selected_files = filedialog.askopenfilenames(title="Select Files")
        self.file_listbox.delete(0, END)
        for f in self.selected_files:
            self.file_listbox.insert(END, os.path.basename(f))

    def select_destination(self):
        self.destination = filedialog.askdirectory(title="Select Destination")
        self.dst_label.config(text=f"Destination: {self.destination}")

    def start_copy_move(self):
        if not self.selected_files or not self.destination:
            messagebox.showerror("Error", "Select files and destination.")
            return
        threading.Thread(target=self.copy_move_files).start()

    def copy_move_files(self):
        for file in self.selected_files:
            try:
                target = os.path.join(self.destination, os.path.basename(file))
                if self.operation.get() == 'copy':
                    shutil.copy(file, target)
                else:
                    shutil.move(file, target)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        messagebox.showinfo("Done", f"Files {self.operation.get()}ed successfully!")

    # ---------- Rename Tab ----------
    def setup_rename_tab(self):
        tab = Frame(self.notebook)
        self.notebook.add(tab, text="Rename")

        Label(tab, text="Select File to Rename").pack(pady=5)
        Button(tab, text="Choose File", command=self.choose_file_to_rename).pack(pady=5)
        self.rename_path_label = Label(tab, text="File: None")
        self.rename_path_label.pack()

        Label(tab, text="Enter New Name (with extension)").pack(pady=5)
        self.new_name_entry = Entry(tab)
        self.new_name_entry.pack(pady=5)

        Button(tab, text="Rename", command=self.rename_file).pack(pady=10)
        self.file_to_rename = ""

    def choose_file_to_rename(self):
        self.file_to_rename = filedialog.askopenfilename()
        self.rename_path_label.config(text=f"File: {self.file_to_rename}")

    def rename_file(self):
        new_name = self.new_name_entry.get().strip()
        if not self.file_to_rename or not new_name:
            messagebox.showerror("Error", "Select a file and provide a new name.")
            return
        folder = os.path.dirname(self.file_to_rename)
        new_path = os.path.join(folder, new_name)
        try:
            os.rename(self.file_to_rename, new_path)
            messagebox.showinfo("Success", "File renamed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Resize Tab ----------
    def setup_resize_tab(self):
        tab = Frame(self.notebook)
        self.notebook.add(tab, text="Resize Images")

        Label(tab, text="Select Folder with Images").pack(pady=5)
        Button(tab, text="Choose Folder", command=self.select_resize_folder).pack(pady=5)
        self.resize_folder_label = Label(tab, text="Folder: Not selected")
        self.resize_folder_label.pack()

        self.width_var = IntVar(value=300)
        self.height_var = IntVar(value=300)
        Label(tab, text="Min Width:").pack()
        Entry(tab, textvariable=self.width_var).pack()
        Label(tab, text="Min Height:").pack()
        Entry(tab, textvariable=self.height_var).pack()

        Button(tab, text="Resize Images", command=self.resize_images).pack(pady=10)
        self.resize_folder = ""

    def select_resize_folder(self):
        self.resize_folder = filedialog.askdirectory()
        self.resize_folder_label.config(text=f"Folder: {self.resize_folder}")

    def resize_images(self):
        if not self.resize_folder:
            messagebox.showerror("Error", "No folder selected")
            return
        threading.Thread(target=self._resize_images).start()

    def _resize_images(self):
        for dirpath, _, files in os.walk(self.resize_folder):
            for file in files:
                path = os.path.join(dirpath, file)
                try:
                    with Image.open(path) as img:
                        w, h = img.size
                        if w < self.width_var.get() or h < self.height_var.get():
                            new_w = max(w, self.width_var.get())
                            new_h = max(h, self.height_var.get())
                            img = img.resize((new_w, new_h))
                            img.save(path)
                except:
                    pass
        messagebox.showinfo("Done", "Image resizing completed.")

    # ---------- Download Tab ----------
    def setup_download_tab(self):
        tab = Frame(self.notebook)
        self.notebook.add(tab, text="Download via URL")

        Label(tab, text="Enter Image URL").pack(pady=5)
        self.url_entry = Entry(tab, width=50)
        self.url_entry.pack(pady=5)

        Label(tab, text="Enter File Name (with extension)").pack(pady=5)
        self.download_name_entry = Entry(tab, width=50)
        self.download_name_entry.pack(pady=5)

        Button(tab, text="Choose Destination Folder", command=self.select_download_folder).pack()
        self.download_folder_label = Label(tab, text="Folder: Not selected")
        self.download_folder_label.pack()

        Button(tab, text="Download", command=self.download_file).pack(pady=10)
        self.download_folder = ""

    def select_download_folder(self):
        self.download_folder = filedialog.askdirectory()
        self.download_folder_label.config(text=f"Folder: {self.download_folder}")

    def download_file(self):
        url = self.url_entry.get().strip()
        name = self.download_name_entry.get().strip()
        if not url or not name or not self.download_folder:
            messagebox.showerror("Error", "Fill all fields and choose folder.")
            return
        try:
            target = os.path.join(self.download_folder, name)
            urllib.request.urlretrieve(url, target)
            messagebox.showinfo("Success", "File downloaded!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Delete / Mkdir Tab ----------
    def setup_delete_mkdir_tab(self):
        tab = Frame(self.notebook)
        self.notebook.add(tab, text="Delete / Mkdir")

        Label(tab, text="Select Files to Delete").pack()
        Button(tab, text="Choose Files", command=self.select_files_to_delete).pack(pady=5)
        Button(tab, text="Delete Selected", command=self.delete_selected_files).pack(pady=5)

        Label(tab, text="Create New Folder Path").pack(pady=10)
        self.mkdir_entry = Entry(tab, width=50)
        self.mkdir_entry.pack()
        Button(tab, text="Create Folder", command=self.create_folder).pack(pady=5)
        self.files_to_delete = []

    def select_files_to_delete(self):
        self.files_to_delete = filedialog.askopenfilenames()
        messagebox.showinfo("Selected", f"{len(self.files_to_delete)} files selected")

    def delete_selected_files(self):
        for f in self.files_to_delete:
            try:
                os.remove(f)
            except:
                pass
        messagebox.showinfo("Deleted", "Files deleted.")

    def create_folder(self):
        path = self.mkdir_entry.get().strip()
        try:
            os.makedirs(path, exist_ok=True)
            messagebox.showinfo("Success", "Folder created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = Tk()
    app = FileManagerApp(root)
    root.mainloop()
