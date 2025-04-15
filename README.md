# BusyLight Desktop

A simple desktop application that shows availability status with a color-coded indicator.

## Features

- Toggle between "Available" and "Busy" status
- Draggable interface
- Always stays on top of other windows
- Resizable
- Remembers position, size and status
- Language switching (Spanish/English)
- System tray integration (when available)

## For Users

### Windows Installation

1. Download the latest `busylight.zip` from the releases section
2. Extract the ZIP file to any location on your computer
3. Run `busylight.exe` from the extracted folder
4. If Windows SmartScreen shows a warning, click "More info" and then "Run anyway"

### Usage

- Left-click to toggle between "Available" and "Busy" status
- Left-click and drag to move the window
- Right-click and drag to resize the window
- Middle-click or press Escape to:
  - Minimize to system tray (when system tray is available)
  - Close the application (when system tray is not available)
- Right-click on the system tray icon for additional options (if available)
  - Show: Restore the window if minimized
  - Toggle Status: Switch between Available/Busy
  - Language: Change between Spanish and English
  - Exit: Close the application

## For Developers

### Project Structure

```
busylight-desktop/
├── .github/workflows/ - CI/CD workflows
├── assets/ - Images and icons
├── build/ - Build configuration
├── src/ - Source code
│   ├── busylight_controller.py - Business logic
│   ├── busylight_ui.py - User interface
│   └── main.py - Application entry point
└── README.md - Documentation
```

### Building from Source

This application is built using Python and Tkinter. The Windows executable is created using Nuitka via GitHub Actions.

#### Prerequisites

- Python 3.8 or higher
- Tkinter (usually included with Python)
- Required packages: `pip install -r requirements.txt`

#### Local Development

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python src/main.py
   ```

#### Building Windows Executable

The Windows executable is automatically built using GitHub Actions. To trigger a build:

1. Push to the main branch, or
2. Go to the Actions tab in GitHub and manually trigger the "Build Windows Executable" workflow

The built executable will be available as an artifact from the workflow run.
