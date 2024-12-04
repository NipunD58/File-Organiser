import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import logging
from datetime import datetime

class FileOrganizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Advanced File Organizer")
        master.geometry("400x500")
        master.resizable(False, False)

        # Configure logging
        self.setup_logging()

        # File Categories (expanded and more comprehensive)
        self.categories = {
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.wma', '.ogg'],
            'Video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Documents': [
                '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', 
                '.xls', '.xlsx', '.ppt', '.pptx', '.pages', '.csv'
            ],
            'Images': [
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', 
                '.webp', '.raw', '.heic', '.svg'
            ],
            'Archives': [
                '.zip', '.rar', '.7z', '.tar.gz', '.tar', '.gz', 
                '.xz', '.bz2', '.tgz'
            ],
            'Programs': [
                '.exe', '.msi', '.dmg', '.app', '.iso', 
                '.bin', '.deb', '.rpm'
            ],
            'Scripts': [
                '.py', '.sh', '.js', '.bat', '.ps1', 
                '.rb', '.pl', '.lua', '.ino'
            ],
            'Databases': ['.sql', '.db', '.sqlite', '.mdb', '.accdb'],
            'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
            'Code': [
                '.html', '.css', '.cpp', '.c', '.java', 
                '.swift', '.go', '.php', '.cs'
            ],
            'Compressed': [
                '.torrent', '.crx', '.pkg'
            ]
        }

        # UI Setup
        self.create_ui()

    def setup_logging(self):
        """Set up logging to track file organization operations."""
        log_dir = Path.home() / 'FileOrganizerLogs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f'file_organizer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        logging.basicConfig(
            filename=log_file, 
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )

    def create_ui(self):
        """Create the user interface."""
        # Folder selection
        tk.Label(self.master, text="Select a folder to organize:", font=("Arial", 12)).pack(pady=(10, 5))
        
        self.folder_var = tk.StringVar()
        self.folder_entry = tk.Entry(self.master, textvariable=self.folder_var, width=50)
        self.folder_entry.pack(pady=5)
        
        select_button = tk.Button(self.master, text="Browse", command=self.select_folder)
        select_button.pack(pady=5)

        # Options Frame
        options_frame = tk.LabelFrame(self.master, text="Organize Options", padx=10, pady=10)
        options_frame.pack(padx=10, pady=10, fill="x")

        # Subcategory checkboxes
        self.subcategory_var = tk.BooleanVar(value=True)
        subcategory_check = tk.Checkbutton(
            options_frame, 
            text="Create Subcategories", 
            variable=self.subcategory_var
        )
        subcategory_check.pack(anchor='w')
        
        # Add a tooltip-like explanation
        tk.Label(
            options_frame, 
            text="(Creates subfolders by file type within main categories)", 
            font=("Arial", 8), 
            fg="gray"
        ).pack(anchor='w')

        # Date-based organization
        self.date_var = tk.BooleanVar(value=False)
        date_check = tk.Checkbutton(
            options_frame, 
            text="Organize by Date (Year/Month)", 
            variable=self.date_var
        )
        date_check.pack(anchor='w')

        # Organize button
        self.organize_button = tk.Button(
            self.master, 
            text="Organize Files", 
            command=self.organize_files, 
            state=tk.DISABLED
        )
        self.organize_button.pack(pady=10)

        # Status area
        self.status_var = tk.StringVar(value="Ready to organize files...")
        status_label = tk.Label(
            self.master, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor='w'
        )
        status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def select_folder(self):
        """Open folder selection dialog."""
        folder_selected = filedialog.askdirectory(title="Select folder to organize")
        if folder_selected:
            self.folder_var.set(folder_selected)
            self.organize_button.config(state=tk.NORMAL)
            self.status_var.set(f"Selected folder: {folder_selected}")

    def organize_files(self):
        """Main file organization method."""
        folder_path = self.folder_var.get()
        if not folder_path:
            messagebox.showerror("Error", "No folder selected.")
            return

        try:
            # Confirm before organizing
            if not messagebox.askyesno("Confirm", f"Are you sure you want to organize files in\n{folder_path}?\n\nWARNING: This will move files around!"):
                return

            # Perform organization
            moved_files, skipped_files = self.organize_directory(folder_path)

            # Log and display results
            logging.info(f"Organized folder: {folder_path}")
            logging.info(f"Moved {moved_files} files")
            logging.info(f"Skipped {skipped_files} files")

            messagebox.showinfo(
                "Organization Complete", 
                f"File organization finished!\n\n"
                f"Moved: {moved_files} files\n"
                f"Skipped: {skipped_files} files\n\n"
                f"Check log for details."
            )
            
            self.status_var.set(f"Organized {moved_files} files. Check log for details.")

        except Exception as e:
            logging.error(f"Error organizing files: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def organize_directory(self, folder_path):
        """
        Organize files in the given directory.
        
        Args:
            folder_path (str): Path to the directory to organize
        
        Returns:
            tuple: (number of moved files, number of skipped files)
        """
        folder = Path(folder_path)
        moved_files = 0
        skipped_files = 0

        # Reverse mapping of extensions to categories
        ext_to_category = {ext: cat for cat, exts in self.categories.items() for ext in exts}

        # Iterate through files
        for file in folder.iterdir():
            if file.is_file():
                # Skip system or hidden files
                if file.name.startswith('.') or file.name == 'desktop.ini':
                    skipped_files += 1
                    continue

                # Get file extension
                file_ext = file.suffix.lower()

                # Determine category
                category = ext_to_category.get(file_ext, 'Others')

                # Prepare destination
                if self.subcategory_var.get():
                    # Subcategory organization
                    dest_folder = folder / category / (file_ext.lstrip('.') if file_ext else 'unknown')
                else:
                    # Simple category organization
                    dest_folder = folder / category

                # Create destination directory if it doesn't exist
                dest_folder.mkdir(parents=True, exist_ok=True)

                # Date-based organization if selected
                if self.date_var.get():
                    modified_time = datetime.fromtimestamp(file.stat().st_mtime)
                    date_folder = dest_folder / str(modified_time.year) / f'{modified_time.month:02d}'
                    date_folder.mkdir(parents=True, exist_ok=True)
                    dest_folder = date_folder

                # Move file
                try:
                    dest_path = dest_folder / file.name
                    
                    # Handle duplicate file names
                    counter = 1
                    while dest_path.exists():
                        dest_path = dest_folder / f"{file.stem}_{counter}{file.suffix}"
                        counter += 1

                    shutil.move(str(file), str(dest_path))
                    moved_files += 1
                    logging.info(f"Moved {file.name} to {dest_path}")

                except Exception as e:
                    logging.error(f"Failed to move {file.name}: {e}")
                    skipped_files += 1

        return moved_files, skipped_files

def main():
    root = tk.Tk()
    root.title("Advanced File Organizer")
    app = FileOrganizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()