
# FileGuard - File Sorter, THIS IS WHAT HAPPENS WHEN IBM BENCHES YOU FOR TOO LONG

**FileGuard** is a file sorting tool that automatically organizes files into designated folders (Downloads, Desktop) and keeps track of sorted files with live updates in the UI. It uses Python with Tkinter for the UI, Watchdog for background monitoring, and Pillow for handling the icon image.

## Features
- Sort files from the **Desktop** and **Downloads** folders into appropriate directories based on file types.
- Live monitoring of the Desktop and Downloads folders for newly created files.
- Display sorted files in a table with the folder and file path.
- Run the application in the background with an option to monitor these folders continuously.


## Requirements

This project requires the following dependencies:

- **Tkinter**: For creating the graphical user interface.
- **Watchdog**: For monitoring changes to the Desktop and Downloads folders.
- **Pillow**: For handling icons.

You can install these dependencies using `requirements.txt`.

## Setup

1. Clone the repository or download the project files to your local machine.
2. Navigate to the project directory in your terminal or command prompt.

### Install Dependencies

Use `pip` to install the required dependencies. Run the following command:

```bash
pip install -r requirements.txt
