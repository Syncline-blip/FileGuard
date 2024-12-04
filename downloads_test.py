import os
from fileguard_logic import organize_files_dynamic

def test_in_downloads():
    """Test the organization functionality in the Downloads folder."""
    downloads_folder = os.path.expanduser("~/Downloads")  # Get the Downloads folder path

    if not os.path.exists(downloads_folder):
        print(f"Error: Downloads folder does not exist at {downloads_folder}")
        return

    print(f"Running FileSweeper in {downloads_folder}...")
    try:
        # Organize files
        organize_files_dynamic(downloads_folder)
        print("Files in Downloads organized successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_in_downloads()
