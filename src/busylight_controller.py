# -*- coding: utf-8 -*-
import os
import sys
import json
import logging

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BusyLightController:
    """Handles business logic"""
    
    def __init__(self, settings_file="busylight_settings.json"):
        """Init controller"""
        self.settings_file = settings_file
        self.settings = self.load_settings()
        
    def toggle_status(self):
        """Toggle status"""
        self.settings['is_available'] = not self.settings['is_available']
        self.save_settings()
        return self.settings['is_available']
    
    def get_status(self):
        """Get current status"""
        return self.settings['is_available']
    
    def get_status_text(self):
        """Get display text"""
        if self.settings['is_available']:
            return self.settings['available_text']
        else:
            return self.settings['busy_text']
    
    def update_window_size(self, width, height):
        """Update size in settings"""
        self.settings['size'] = f"{width}x{height}"
        self.save_settings()
    
    def update_window_position(self, x, y):
        """Update position in settings"""
        self.settings['position'] = f"+{x}+{y}"
        self.save_settings()
    
    def get_settings(self):
        """Get all settings"""
        return self.settings
    
    def update_setting(self, key, value):
        """Update a setting"""
        if key in self.settings:
            self.settings[key] = value
            self.save_settings()
    
    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            'size': "300x80",
            'position': "+100+100",
            'is_available': True,
            'available_text': "DISPONIBLE",
            'busy_text': "OCUPADO",
            'use_tray': True
        }
        
        try:
            # get app directory
            app_dir = self._get_app_directory()
            settings_path = os.path.join(app_dir, self.settings_file)
            
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    loaded_settings = json.load(f)
                    # merge with defaults for backward compatibility
                    for key, value in default_settings.items():
                        if key not in loaded_settings:
                            loaded_settings[key] = value
                    return loaded_settings
            return default_settings
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            app_dir = self._get_app_directory()
            settings_path = os.path.join(app_dir, self.settings_file)
            
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f)
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def _get_app_directory(self):
        """Get app directory"""
        if getattr(sys, 'frozen', False):
            # running as exe
            return os.path.dirname(sys.executable)
        else:
            # running as script
            return os.path.dirname(os.path.abspath(__file__))
