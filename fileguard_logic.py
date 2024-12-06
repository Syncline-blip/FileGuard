import os
import shutil
from pathlib import Path
import mimetypes
from collections import defaultdict

# File Categories
FILE_CATEGORIES = {
    "Documents": [".pdf", ".docx", ".txt", ".xls", ".xlsx"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Compressed": [".zip", ".rar", ".7z", ".gz"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".flac", ".aac"]
}

# Dynamic Categorisation
def categorise_extension_dynamic(file_ext, file_path):
    for category, extensions in FILE_CATEGORIES.items():
        if file_ext.lower() in extensions:
            return category
    
    # Check mime type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type.startswith("audio"):
            return "Music"
        elif mime_type.startswith("video"):
            return "Videos"
        elif mime_type.startswith("image"):
            return "Pictures"
        elif mime_type.startswith("text"):
            return "Documents"
        elif mime_type.startswith("application"):
            # Special case: check for compressed files
            if "zip" in mime_type or "x-rar" in mime_type:
                return "Compressed"
    return "Others"


# Check if the folders exists and create folders based on files in the directory
def folder_setup(folder_path, category_map):
    """Create folders only if there are files of that category."""
    # Ensure category folders exist for categories with files
    for category, files in category_map.items():
        category_path = os.path.join(folder_path, category)
        if not os.path.exists(category_path):  # Only create if the folder doesn't exist
            os.makedirs(category_path)
    
    others_path = os.path.join(folder_path, "Others")
    if "Others" in category_map and not os.path.exists(others_path):
        os.makedirs(others_path)


def organize_files_dynamic(folder_path):
    """Dynamically organizes files in the given folder into categories."""
    category_map = defaultdict(list)  # Map category names to their files

    # Iterate over the files in the directory
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            file_ext = Path(file).suffix
            category = categorise_extension_dynamic(file_ext, file_path)
            category_map[category].append(file_path)

    # Ensure category folders exist
    folder_setup(folder_path, category_map)

    # Move files into their respective categories
    for category, files in category_map.items():
        category_path = os.path.join(folder_path, category)
        for file_path in files:
            shutil.move(file_path, os.path.join(category_path, os.path.basename(file_path)))

    print(f"Organized files into {len(category_map)} categories.")


def is_file_incomplete(file_path):
    """Check if the file is incomplete based on known temporary extensions."""
    incomplete_extensions = ['.crdownload', '.part']
    return any(file_path.endswith(ext) for ext in incomplete_extensions)
