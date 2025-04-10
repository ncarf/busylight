# BusyLight Desktop

A simple desktop application that shows availability status with a color-coded indicator.

## Features

- Toggle between "Available" and "Busy" status
- Draggable interface
- Always stays on top of other windows
- Resizable

## For Users

### Windows Installation

1. Download the latest `BusyLight-Windows.zip` from the releases section
2. Extract the ZIP file to any location on your computer
3. Run `BusyLight.exe` from the extracted folder
4. If Windows SmartScreen shows a warning, click "More info" and then "Run anyway"

### Usage

- Click on the indicator to toggle between "Available" and "Busy" status
- Click and drag to move the window
- Resize the window as needed

## For Developers

### Building from Source

This application is built using Python and Tkinter. The Windows executable is created using Nuitka via GitHub Actions.

#### Prerequisites

- Python 3.8 or higher
- Tkinter (usually included with Python)

#### Local Development

1. Clone the repository
2. Run the application:
   ```
   python src/busylight.py
   ```

#### Building Windows Executable

The Windows executable is automatically built using GitHub Actions. To trigger a build:

1. Push to the main branch, or
2. Go to the Actions tab in GitHub and manually trigger the "Build Windows Executable" workflow

The built executable will be available as an artifact from the workflow run.
