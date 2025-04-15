# -*- coding: utf-8 -*-
from busylight_controller import BusyLightController
from busylight_ui import BusyLightUI
import logging

# setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    try:
        controller = BusyLightController()
        app = BusyLightUI(controller)
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main()
