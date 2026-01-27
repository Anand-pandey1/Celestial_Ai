# UI/floating_panel.py
import tkinter as tk

class FloatingPanel:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Celestial AI")
        self.root.overrideredirect(True)  # no window border
        self.root.attributes("-topmost", True)

        # Panel size & position (left side, middle)
        width = 260
        height = 80
        screen_h = self.root.winfo_screenheight()
        x = 20
        y = int((screen_h / 2) - (height / 2))

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.configure(bg="#111111")

        label = tk.Label(
            self.root,
            text="🌌 Celestial AI",
            fg="white",
            bg="#111111",
            font=("Segoe UI", 14, "bold")
        )
        label.pack(expand=True)

    def run(self):
        self.root.mainloop()


def start_ui():
    panel = FloatingPanel()
    panel.run()
