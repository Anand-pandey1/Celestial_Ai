# UI/floating_panel.py
import tkinter as tk

class FloatingPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#111111")

        self.visible = True
        self.voice_enabled = True
        self.camera_on = False

        # Position
        width, height = 300, 260
        x, y = 20, 200
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Title
        self.title = tk.Label(
            self.root, text="⭕ Celestial AI",
            fg="white", bg="#111111",
            font=("Segoe UI", 15, "bold")
        )
        self.title.pack(pady=(8, 2))

        # Status with text wrapping
        self.status = tk.Label(
            self.root, text="Status: Listening",
            fg="#bbbbbb", bg="#111111",
            font=("Segoe UI", 10),
            wraplength=280,
            justify="left"
        )
        self.status.pack(pady=4, padx=5)

        # Command entry
        self.entry = tk.Entry(
            self.root,
            bg="#222222",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.entry.pack(fill="x", padx=10, pady=(4, 2))

        self.entry.bind("<Return>", self.submit_command)
        # callback
        self.on_command_submit = None

        # Buttons
        self.btn_voice = tk.Button(
            self.root, text="🎤 Voice: ON",
            command=self.toggle_voice,
            bg="#222222", fg="white", relief="flat"
        )
        self.btn_voice.pack(fill="x", padx=10, pady=4)

        self.btn_camera = tk.Button(
            self.root, text="📷 Camera: OFF",
            command=self.toggle_camera,
            bg="#222222", fg="white", relief="flat"
        )
        self.btn_camera.pack(fill="x", padx=10)

        # Drag support
        self.title.bind("<ButtonPress-1>", self.start_move)
        self.title.bind("<B1-Motion>", self.do_move)
        self.x_offset = 0
        self.y_offset = 0

        # Callbacks (set by core)
        self.on_voice_toggle = None
        self.on_camera_toggle = None

    def start_move(self, e):
        self.x_offset = e.x
        self.y_offset = e.y

    def do_move(self, e):
        x = self.root.winfo_pointerx() - self.x_offset
        y = self.root.winfo_pointery() - self.y_offset
        self.root.geometry(f"+{x}+{y}")

    def submit_command(self, event):
        text = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if text and self.on_command_submit:
            self.on_command_submit(text)

    # ---- UI State Updates ----
    def set_status(self, text):
        self.status.config(text=f"Status: {text}")

    def toggle(self):
        self.root.withdraw() if self.visible else self.root.deiconify()
        self.visible = not self.visible

    # ---- Button Actions ----
    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        self.btn_voice.config(
            text=f"🎤 Voice: {'ON' if self.voice_enabled else 'OFF'}"
        )
        if self.on_voice_toggle:
            self.on_voice_toggle(self.voice_enabled)

    def toggle_camera(self):
        self.camera_on = not self.camera_on
        self.btn_camera.config(
            text=f"📷 Camera: {'ON' if self.camera_on else 'OFF'}"
        )
        if self.on_camera_toggle:
            self.on_camera_toggle(self.camera_on)

    def run(self):
        self.root.mainloop()


_panel = None

def start_ui(voice_cb=None, camera_cb=None, command_cb=None):
    global _panel
    _panel = FloatingPanel()
    if voice_cb:
        _panel.on_voice_toggle = voice_cb
    if camera_cb:
        _panel.on_camera_toggle = camera_cb
    if command_cb:
        _panel.on_command_submit = command_cb
    _panel.run()

def update_status(text):
    if _panel:
        _panel.set_status(text)

def toggle_ui():
    if _panel:
        _panel.toggle()

def register_callbacks(voice_cb, camera_cb, command_cb):
    if _panel:
        _panel.on_voice_toggle = voice_cb
        _panel.on_camera_toggle = camera_cb
        _panel.on_command_submit = command_cb

