# -*- coding: utf-8 -*-
import tkinter as tk
import sys
import os
import threading
import logging
import platform

# constants
AVAILABLE_COLOR = "#4CAF50"
BUSY_COLOR = "#F44336"
MIN_WIDTH = 100
MIN_HEIGHT = 40
FONT_FAMILY = "Helvetica"
FONT_STYLE = "bold"
MIN_FONT_SIZE = 10

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"

TRAY_AVAILABLE = False
try:
    from PIL import Image
    import pystray

    TRAY_AVAILABLE = True
except ImportError:
    logger.warning("System tray dependencies not available. Running without tray icon.")
except Exception as e:
    logger.warning(f"Error importing system tray dependencies: {e}")


class BusyLightUI(tk.Tk):
    """UI for BusyLight"""

    def __init__(self, controller):
        """Init UI"""
        super().__init__()
        self.controller = controller
        self.is_moving = False
        self.tray_icon = None
        self.tray_thread = None
        self.has_tray = False

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        settings = self.controller.get_settings()
        self.geometry(f"{settings['size']}{settings['position']}")

        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.configure(bg="#FFFFFF")

        if IS_WINDOWS:
            try:
                import ctypes
                from ctypes import windll

                hwnd = windll.user32.GetParent(self.winfo_id())
                style = windll.dwmapi.DwmSetWindowAttribute
                DWMWA_WINDOW_CORNER_PREFERENCE = 33
                DWM_WINDOW_CORNER_PREFERENCE = 2  # rounded
                style(
                    hwnd,
                    DWMWA_WINDOW_CORNER_PREFERENCE,
                    ctypes.byref(ctypes.c_int(DWM_WINDOW_CORNER_PREFERENCE)),
                    ctypes.sizeof(ctypes.c_int),
                )
            except Exception as e:
                logger.warning(f"failed to set rounded corners: {e}")

        width, height = map(int, settings["size"].split("x"))

        self.label = tk.Label(
            self,
            text=self.controller.get_status_text(),
            fg="#FFFFFF",
            bg=self._get_status_color(),
            font=(FONT_FAMILY, self._get_font_size(width, height), FONT_STYLE),
            pady=20,
            cursor="hand2",
        )
        self.label.pack(expand=True, fill="both")

        self.last_width = width
        self.last_height = height

        self.bind_common_events()

        if TRAY_AVAILABLE and settings.get("use_tray", True):
            self.setup_tray_icon()
        else:
            self.setup_window_controls(False)

    def _get_font_size(self, width, height):
        """Get appropriate font size"""
        font_size = min(width // 8, height // 3)
        return max(font_size, MIN_FONT_SIZE)

    def bind_common_events(self):
        """Bind events common to all platforms"""
        # movement and resizing
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.on_move)
        self.label.bind("<ButtonRelease-1>", self.toggle_status)
        self.label.bind("<Button-3>", self.start_resize)
        self.label.bind("<B3-Motion>", self.on_resize)
        self.bind("<Configure>", self.on_configure)

        # add both Button-2 and Button-4 for middle click (works better across platforms)
        self.label.bind("<Button-2>", self._handle_middle_click)
        self.label.bind("<Button-4>", self._handle_middle_click)

    def setup_window_controls(self, has_tray):
        """Setup window controls based on tray availability"""
        self.has_tray = has_tray

        if has_tray:
            self.bind("<Escape>", self.minimize_to_tray)
            self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
            logger.info("Window controls set for system tray mode")
        else:
            self.bind("<Escape>", self.quit_app)
            self.protocol("WM_DELETE_WINDOW", self.quit_app)
            logger.info("Window controls set for standalone mode")

    def start_move(self, event):
        """Prepare for movement"""
        self.x_offset = event.x
        self.y_offset = event.y
        self.is_moving = False
        self.start_x = event.x_root
        self.start_y = event.y_root

    def on_move(self, event):
        """Handle movement"""
        x = self.winfo_x() + (event.x - self.x_offset)
        y = self.winfo_y() + (event.y - self.y_offset)
        self.geometry(f"+{x}+{y}")
        self.is_moving = True

    def toggle_status(self, event):
        """Toggle if not moving"""
        if not self.is_moving or (
            abs(event.x_root - self.start_x) < 5
            and abs(event.y_root - self.start_y) < 5
        ):
            self.controller.toggle_status()
            self.update_display()
            self.update_tray_icon()

    def start_resize(self, event):
        """Prepare for resize"""
        self.x_resize = event.x_root
        self.y_resize = event.y_root
        self.width = self.winfo_width()
        self.height = self.winfo_height()

    def on_resize(self, event):
        """Handle resize"""
        width_diff = event.x_root - self.x_resize
        height_diff = event.y_root - self.y_resize

        new_width = max(self.width + width_diff, MIN_WIDTH)
        new_height = max(self.height + height_diff, MIN_HEIGHT)

        self.geometry(f"{new_width}x{new_height}")
        self.controller.update_window_size(new_width, new_height)

    def on_configure(self, event):
        """Handle window changes"""
        if hasattr(self, "last_width") and hasattr(self, "last_height"):
            if self.last_width != event.width or self.last_height != event.height:
                self.resize_font(event)

        self.controller.update_window_position(self.winfo_x(), self.winfo_y())

        self.last_width = event.width
        self.last_height = event.height

    def resize_font(self, event):
        """Adjust font size"""
        font_size = self._get_font_size(event.width, event.height)
        self.label.configure(font=(FONT_FAMILY, font_size, FONT_STYLE))

    def update_display(self):
        """Update display"""
        self.label.configure(
            text=self.controller.get_status_text(), bg=self._get_status_color()
        )

    def _get_status_color(self):
        """Get status color"""
        return AVAILABLE_COLOR if self.controller.get_status() else BUSY_COLOR

    def setup_tray_icon(self):
        """Setup system tray icon"""
        try:
            if IS_LINUX:
                desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "")
                session_type = os.environ.get("XDG_SESSION_TYPE", "")

                if session_type.lower() == "wayland":
                    logger.warning("wayland detected, skipping tray")
                    self.setup_window_controls(False)
                    return

                if not desktop_env or desktop_env.lower() in ["gnome", "ubuntu:gnome"]:
                    logger.warning(f"unsupported desktop: {desktop_env}")
                    self.setup_window_controls(False)
                    return

            self._setup_tray_thread()
        except Exception as e:
            logger.error(f"tray setup error: {e}")
            self.setup_window_controls(False)

    def _setup_tray_thread(self):
        """Create tray icon in a separate thread"""
        self.tray_thread = threading.Thread(target=self._create_tray_icon)
        self.tray_thread.daemon = True
        self.tray_thread.start()

    def _create_tray_icon(self):
        """Create the system tray icon"""
        try:
            # get icon path
            if getattr(sys, "frozen", False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_dir, "assets", "busylight.ico")
            icon_image = (
                Image.open(icon_path)
                if os.path.exists(icon_path)
                else self._create_default_icon()
            )

            # language menu setup
            languages = self.controller.get_available_languages()
            language_menu = []

            def make_language_handler(lang_code):
                return lambda icon, item: self._change_language(lang_code)

            for code, name in languages.items():
                language_menu.append(
                    pystray.MenuItem(name, make_language_handler(code))
                )

            menu = (
                pystray.MenuItem("Show", self._show_window),
                pystray.MenuItem("Toggle Status", self._toggle_status_from_tray),
                pystray.MenuItem("Language", pystray.Menu(*language_menu)),
                pystray.MenuItem("Exit", self._quit_app),
            )

            # create icon but don't enable tray mode yet
            self.tray_icon = pystray.Icon("busylight", icon_image, "BusyLight", menu)
            self.update_tray_icon()

            # disable tray mode if icon.run() fails
            try:
                self.tray_icon.run()
            except Exception as e:
                logger.warning(f"tray unavailable: {e}")
                self.after(0, lambda: self.setup_window_controls(False))
                return

            # tray is working
            self.after(0, lambda: self.setup_window_controls(True))
        except Exception as e:
            logger.error(f"tray error: {e}")
            self.after(0, lambda: self.setup_window_controls(False))

    def _create_default_icon(self):
        """Create a default icon if the icon file is not found"""
        try:
            from PIL import ImageDraw

            img = Image.new("RGBA", (64, 64), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            color = self._get_status_color()
            if color.startswith("#"):
                color = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))

            draw.ellipse((4, 4, 60, 60), fill=color)
            return img
        except Exception as e:
            logger.error(f"Error creating default icon: {e}")
            return None

    def update_tray_icon(self):
        """Update tray icon based on status"""
        if not self.has_tray or not self.tray_icon:
            return

        try:
            status_text = "Available" if self.controller.get_status() else "Busy"
            self.tray_icon.title = f"BusyLight - {status_text}"

            from PIL import ImageDraw

            img = Image.new("RGBA", (64, 64), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            color = self._get_status_color()
            if color.startswith("#"):
                color = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))

            draw.ellipse((4, 4, 60, 60), fill=color)
            self.tray_icon.icon = img
        except Exception as e:
            logger.warning(f"Error updating tray icon: {e}")

    def _show_window(self, icon, item):
        """Show the window from tray"""
        try:
            self.deiconify()
            self.attributes("-topmost", True)
            self.attributes("-topmost", False)
        except Exception as e:
            logger.error(f"Error showing window: {e}")

    def _toggle_status_from_tray(self, icon, item):
        """Toggle status from tray"""
        try:
            self.controller.toggle_status()
            self.update_display()
            self.update_tray_icon()
        except Exception as e:
            logger.error(f"Error toggling status from tray: {e}")

    def _change_language(self, lang_code):
        """Change language"""
        try:
            self.controller.set_language(lang_code)
            self.update_display()
        except Exception as e:
            logger.error(f"Error changing language: {e}")

    def minimize_to_tray(self, event=None):
        """Minimize to system tray"""
        if not self.has_tray:
            return

        try:
            self.withdraw()
        except Exception as e:
            logger.error(f"Error minimizing to tray: {e}")
            self.deiconify()
        return "break"

    def _quit_app(self, icon=None, item=None):
        """Quit the application from tray"""
        try:
            if self.tray_icon:
                self.tray_icon.stop()
        except Exception as e:
            logger.error(f"Error stopping tray icon: {e}")
        finally:
            self.quit_app()

    def quit_app(self, event=None):
        """Close app"""
        try:
            if hasattr(self, "tray_icon") and self.tray_icon:
                try:
                    self.tray_icon.stop()
                except:
                    pass
        finally:
            self.destroy()
            sys.exit()

    def _handle_middle_click(self, event):
        """Handle middle click based on tray availability"""
        if self.has_tray:
            self.minimize_to_tray()
        else:
            self.quit_app()
        return "break"
