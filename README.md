# BusyLight

A simple visual status indicator for your desktop. Shows colleagues when you're available or need focus time.

<img src="assets/busylight_small.gif" alt="BusyLight in action" width="700">

## What it does

BusyLight displays a colored indicator on your screen that changes between "Available" (green) and "Busy" (red). It stays on top of other windows but remains unobtrusive, letting people around you know your availability at a glance.

## Features

- Click to toggle between Available and Busy states
- Drag to move anywhere on screen
- Right-click and drag to resize
- Minimize to system tray (middle-click or Escape)
- Remembers position and size between sessions
- English and Spanish language support
- System tray icon changes color with status

## Installation

### Windows

1. Download `busylight.zip` from the [releases page](https://github.com/ncarf/busylight/releases)
2. Extract anywhere on your computer
3. Run `busylight.exe`

## Usage

- **Left-click**: Toggle status
- **Left-click + drag**: Move window
- **Right-click + drag**: Resize window
- **Middle-click** or **Escape**: Minimize to tray
- **Right-click tray icon**: Access menu options

## Use cases

- Remote work with shared spaces
- Open office environments
- Video calls and meetings
- Deep work sessions
- Hot-desking setups

## Development

Built with Python and Tkinter. Uses PyInstaller for Windows executable creation.

```bash
# Run from source
python src/main.py

# Build executable
pyinstaller busylight.spec
```
