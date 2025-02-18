import tkinter as tk

class BusyLightWidget(tk.Tk):
    def __init__(self):
        super().__init__()
        self.is_available = True
        self.is_moving = False
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.geometry("300x80+100+100")
        self.minsize(100, 40)
        self.configure(bg="#FFFFFF")

        self.label = tk.Label(
            self,
            text="DISPONIBLE",
            fg="#FFFFFF",
            bg="#4CAF50",
            font=("Helvetica", 24, "bold"),
            pady=20,
            cursor="hand2"
        )
        self.label.pack(expand=True, fill="both")

        self.bind_events()
        self.update_status_display()

    def bind_events(self):
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.on_move)
        self.label.bind("<ButtonRelease-1>", self.toggle_status)
        self.bind("<Configure>", self.resize)

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y
        self.is_moving = False

    def on_move(self, event):
        x = self.winfo_x() + (event.x - self.x_offset)
        y = self.winfo_y() + (event.y - self.y_offset)
        self.geometry(f"+{x}+{y}")
        self.is_moving = True

    def toggle_status(self, event):
        if not self.is_moving:
            self.is_available = not self.is_available
            self.update_status_display()

    def resize(self, event):
        width = event.width
        height = event.height
        font_size = min(width // 8, height // 3)
        self.label.configure(font=("Helvetica", font_size, "bold"))

    def update_status_display(self):
        if self.is_available:
            text = "DISPONIBLE"
            bg_color = "#4CAF50"
        else:
            text = "OCUPADO"
            bg_color = "#F44336"
        self.label.configure(text=text, bg=bg_color)


if __name__ == "__main__":
    app = BusyLightWidget()
    app.mainloop()