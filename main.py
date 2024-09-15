import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def organize_files(folder_path):
    folder = Path(folder_path)
    if not folder.is_dir():
        messagebox.showerror("Error", f"{folder_path} is not a valid directory.")
        return

    # Define file type categories
    categories = {
        'Audio': ['.mp3', '.wav', '.flac', '.aac'],
        'Video': ['.mp4', '.avi', '.mkv', '.mov'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt'],
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Archives': ['.zip', '.rar', '.7z', '.tar.gz'],
        'Programs': ['.exe', '.msi', '.dmg', '.app'],
        'Scripts': ['.py', '.sh', '.js', '.bat', '.ino'],
        'Databases': ['.sql', '.db', '.sqlite', '.mdb'],
        'Fonts': ['.ttf', '.otf', '.woff', '.woff2'],
        'Icons': ['.ico'],
        'Others': ['.torrent'],
    }

    def organize_remaining_files(folder):
        moved_files = 0
        existing_folders = [d.name for d in folder.iterdir() if d.is_dir()]
        
        # Create a reverse mapping of extensions to categories
        extension_to_category = {ext: cat for cat, exts in categories.items() for ext in exts}
        
        for file in folder.iterdir():
            if file.is_file():
                file_extension = file.suffix.lower()
                category = extension_to_category.get(file_extension)
                if category and category in existing_folders:
                    destination = folder / category / file.name
                    shutil.move(str(file), str(destination))
                    moved_files += 1
        
        return moved_files

    # Organize files
    moved_files = organize_remaining_files(folder)

    messagebox.showinfo("Complete", f"File organization complete! Moved {moved_files} files.")

# ... rest of the code remains unchanged ...

class FileOrganizerApp:
    def __init__(self, master):
        self.master = master
        master.title("File Organizer")
        master.geometry("300x150")

        self.label = tk.Label(master, text="Select a folder to organize:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)

        self.organize_button = tk.Button(master, text="Organize Files", command=self.organize, state=tk.DISABLED)
        self.organize_button.pack(pady=10)

        self.selected_folder = None

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory(title="Select folder to organize")
        if self.selected_folder:
            self.organize_button.config(state=tk.NORMAL)
            self.label.config(text=f"Selected: {self.selected_folder}")

    def organize(self):
        if self.selected_folder:
            organize_files(self.selected_folder)
        else:
            messagebox.showerror("Error", "No folder selected.")

root = tk.Tk()
app = FileOrganizerApp(root)
root.mainloop()

