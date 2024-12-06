import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from fileguard_logic import organize_files_dynamic, is_file_incomplete
import time

class FileHandler(FileSystemEventHandler):
    """Handles file system events for background monitoring."""
    def __init__(self, folder_path, app):
        self.folder_path = folder_path
        self.app = app

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            retries = 5  # Number of retries
            delay = 2  # Time to wait between retries (in seconds)

            # Wait for the file to become available and fully written
            while retries > 0:
                if os.path.exists(file_path) and not is_file_incomplete(file_path):
                    try:
                        initial_size = os.path.getsize(file_path)
                        # Wait a bit to check if the file size stabilizes
                        time.sleep(2)
                        if os.path.getsize(file_path) == initial_size:  # If size is stable, file is fully downloaded
                            organize_files_dynamic(self.folder_path)
                            self.app.update_sorted_files(self.folder_path, file_path)
                            break
                    except OSError:
                        pass  # File may still be temporarily locked, retry after delay
                retries -= 1
                time.sleep(delay)  # Wait before retrying


class FileGuardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileGuard")
       
        
    
        # Set a default size for the window and prevent resizing
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        if getattr(sys, 'frozen', False):  # Check if the app is running as a bundled executable
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            icon_path = 'icon.ico'  # Path to icon for development

        self.root.iconbitmap(icon_path)
        # Use modern font
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 12), padding=10)
        self.style.configure("TLabel", font=("Segoe UI", 12))
        self.style.configure("TTreeview", font=("Segoe UI", 10), rowheight=30)
        self.style.configure("TCheckbutton", font=("Segoe UI", 12))

        # Main frame setup
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configure grid layout for responsiveness
        self.main_frame.grid_columnconfigure(0, weight=1, minsize=200)  # Left side for buttons
        self.main_frame.grid_columnconfigure(1, weight=3, minsize=600)  # Right side for Treeview
        self.main_frame.grid_rowconfigure(0, weight=1)  # Make sure the top row expands

        # Button frame for left side buttons
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # Sorted files frame for Treeview on the right
        self.sorted_files_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.sorted_files_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Add Buttons with rounded, modern style
        self.desktop_button = ttk.Button(self.button_frame, text="Sort Desktop", command=self.sort_desktop)
        self.desktop_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.downloads_button = ttk.Button(self.button_frame, text="Sort Downloads", command=self.sort_downloads)
        self.downloads_button.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        
        self.target_folder_button = ttk.Button(self.button_frame, text="Select Folder to Sort", command=self.sort_target)
        self.target_folder_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        self.background_var = tk.BooleanVar()
        self.background_check = ttk.Checkbutton(
            self.button_frame, text="Run in Background", variable=self.background_var, command=self.toggle_background
        )
        self.background_check.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        # Status Label with green color for idle
        self.status_label = ttk.Label(self.button_frame, text="Idle", foreground="green", width=25, anchor="w")
        self.status_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        # Live list of sorted files with two columns (on the right side)
        self.sorted_files_label = ttk.Label(self.sorted_files_frame, text="Sorted Files:", font=("Segoe UI", 14))
        self.sorted_files_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Treeview setup for displaying sorted files
        self.treeview = ttk.Treeview(self.sorted_files_frame, columns=("Folder", "File Path"), show="headings", height=15)
        self.treeview.heading("Folder", text="Folder")
        self.treeview.heading("File Path", text="File Path")
        self.treeview.column("Folder", width=150)
        self.treeview.column("File Path", width=300)
        self.treeview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        
        # Apply some additional styling for rows
        self.treeview.tag_configure("even", background="#f9f9f9")
        self.treeview.tag_configure("odd", background="#ffffff")

        # Watchdog Observer
        self.observer = None

    def update_sorted_files(self, folder_path):
        """Update Treeview with files sorted into categories."""
        # Clear existing treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        files_found = False  # Flag to track if files are found

        # Iterate through the categories in the folder
        for category in os.listdir(folder_path):
            category_path = os.path.join(folder_path, category)
            if os.path.isdir(category_path):  # Ensure we're checking a directory
                category_found = False  # Track if files were found in a category
                for file_name in os.listdir(category_path):
                    file_path = os.path.join(category_path, file_name)
                    # Ensure it's a file and not a folder
                    if os.path.isfile(file_path):
                        # Insert the file into the treeview
                        self.treeview.insert("", tk.END, values=(category, file_path))
                        category_found = True

                # If files were found in this category, mark it as found
                if category_found:
                    files_found = True

        # If no files were found, insert a message to indicate that
        if not files_found:
            self.treeview.insert("", tk.END, values=("No files found", ""))





    

    def sort_desktop(self):
        desktop_folder = os.path.expanduser("~/Desktop")
        self.sort_folder(desktop_folder)

    def sort_downloads(self):
        downloads_folder = os.path.expanduser("~/Downloads")
        self.sort_folder(downloads_folder)

    def sort_target(self):
        target_folder = filedialog.askdirectory(title="Select Folder to sort")
        if target_folder:
            self.sort_folder(target_folder)

    def sort_folder(self, folder_path):
        try:
            # Check if there are any files to sort
            files_to_sort = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            
            if not files_to_sort:
                # If no files to sort, update the status and do nothing
                self.status_label.config(text="No files to sort in this directory", foreground="red")
                return

            # Proceed with sorting only if there are files to sort
            organize_files_dynamic(folder_path)
            self.update_sorted_files(folder_path)
            self.status_label.config(text=f"{os.path.basename(folder_path)} sorted!", foreground="green")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort {folder_path}: {e}")

    def toggle_background(self):
        if self.background_var.get():
            self.start_background_monitoring()
            self.status_label.config(text="Live Check ON", foreground="Green")
        else:
            self.stop_background_monitoring()
            self.status_label.config(text="Live Check OFF", foreground="Red")

    def start_background_monitoring(self):
        desktop_folder = os.path.expanduser("~/Desktop")
        downloads_folder = os.path.expanduser("~/Downloads")
        self.observer = Observer()
        self.observer.schedule(FileHandler(desktop_folder, self), desktop_folder, recursive=False)
        self.observer.schedule(FileHandler(downloads_folder, self), downloads_folder, recursive=False)
        self.observer.start()

    def stop_background_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

    def on_close(self):
        self.stop_background_monitoring()
        self.root.destroy()

# RUNNNN
if __name__ == "__main__":
    root = tk.Tk()
    app = FileGuardApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
