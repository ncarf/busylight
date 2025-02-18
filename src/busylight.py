import tkinter as tk

class BusyLightWidget(tk.Tk):
    def __init__(self):
        super().__init__()
        self.is_available = True
        self.x_offset = 0
        self.y_offset = 0

        self.configure(bg="green")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.geometry("150x50+100+100")

        self.label = tk.Label(
            self,
            text="DISPONIBLE",
            bg="green",
            fg="white",
            font=("Arial", 12, "bold")
         )
        self.label.pack(expand=True, fill="both")

        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.on_move)
        self.label.bind("<ButtonRelease-1>", self.toggle_status)

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y
        
    def on_move(self, event):
        x = self.winfo_x() + (event.x - self.x_offset)
        y = self.winfo_y() + (event.y - self.y_offset)
        self.geometry(f"+{x}+{y}")
        
    def toggle_status(self, event):
        self.is_available = not self.is_available
        color = "green" if self.is_available else "red"
        text = "DISPONIBLE" if self.is_available else "OCUPADO"
        self.configure(bg=color)
        self.label.configure(bg=color, text=text)

        
if __name__ == "__main__":
    app = BusyLightWidget()
    app.mainloop()        




