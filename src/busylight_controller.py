# -*- coding: utf-8 -*-
import os
import sys
import json
import logging

# setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BusyLightController:
    """Handles business logic"""

    # language dictionaries
    LANGUAGES = {
        "es": {
            "available_text": "DISPONIBLE",
            "busy_text": "OCUPADO",
            "language_name": "Español",
        },
        "en": {
            "available_text": "AVAILABLE",
            "busy_text": "BUSY",
            "language_name": "English",
        },
    }

    def __init__(self):
        """Init controller"""
        # default settings in memory
        self.settings = {
            "size": "300x80",
            "position": "+100+100",
            "is_available": True,
            "language": "es",  # spanish by default
            "use_tray": True,
        }

    def toggle_status(self):
        """Toggle status"""
        self.settings["is_available"] = not self.settings["is_available"]
        return self.settings["is_available"]

    def get_status(self):
        """Get current status"""
        return self.settings["is_available"]

    def get_status_text(self):
        """Get display text"""
        lang = self.settings["language"]
        if self.settings["is_available"]:
            return self.LANGUAGES[lang]["available_text"]
        else:
            return self.LANGUAGES[lang]["busy_text"]

    def set_language(self, lang_code):
        """Set language"""
        if lang_code in self.LANGUAGES:
            self.settings["language"] = lang_code
            return True
        return False

    def get_language(self):
        """Get current language code"""
        return self.settings["language"]

    def get_language_name(self):
        """Get current language name"""
        return self.LANGUAGES[self.settings["language"]]["language_name"]

    def get_available_languages(self):
        """Get list of available languages"""
        return {code: data["language_name"] for code, data in self.LANGUAGES.items()}

    def update_window_size(self, width, height):
        """Update size in settings"""
        self.settings["size"] = f"{width}x{height}"

    def update_window_position(self, x, y):
        """Update position in settings"""
        self.settings["position"] = f"+{x}+{y}"

    def get_settings(self):
        """Get all settings"""
        return self.settings

    def update_setting(self, key, value):
        """Update a setting"""
        if key in self.settings:
            self.settings[key] = value
