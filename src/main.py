# -*- coding: utf-8 -*-
from busylight_controller import BusyLightController
from busylight_ui import BusyLightUI

if __name__ == "__main__":
    # create controller
    controller = BusyLightController()

    # create and start ui
    app = BusyLightUI(controller)
    app.mainloop()
