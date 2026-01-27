# UI/floating_panel.py
import tkinter as tk

class FloatingPanel:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Celestial AI")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.visible = True

        # Panel size & position
        width = 260
        height = 90
        screen_h = self.root.winfo_screenheight()
        x = 20
        y = int((screen_h / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.configure(bg="#111111")

        # Title
        self.title = tk.Label(
            self.root,
            text="⭕ Celestial AI",
            fg="white",
            bg="#111111",
            font=("Segoe UI", 14, "bold")
        )
        self.title.pack(pady=(10, 0))

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Status: Listening",
            fg="#bbbbbb",
            bg="#111111",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(pady=(4, 8))

        # Drag support
        self.title.bind("<ButtonPress-1>", self.start_move)
        self.title.bind("<B1-Motion>", self.do_move)

        self.x_offset = 0
        self.y_offset = 0

    # 🖱️ Drag window
    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.x_offset
        y = self.root.winfo_pointery() - self.y_offset
        self.root.geometry(f"+{x}+{y}")

    # 🔄 Update status text
    def set_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    # 👁️ Toggle visibility
    def toggle(self):
        if self.visible:
            self.root.withdraw()
        else:
            self.root.deiconify()
        self.visible = not self.visible

    def run(self):
        self.root.mainloop()


# Global panel instance
_panel = None

def start_ui():
    global _panel
    _panel = FloatingPanel()
    _panel.run()

def update_status(text: str):
    if _panel:
        _panel.set_status(text)

def toggle_ui():
    if _panel:
        _panel.toggle()
