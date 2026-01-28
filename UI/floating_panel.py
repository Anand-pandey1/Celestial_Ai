# UI/floating_panel.py
import tkinter as tk

class FloatingPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.98)  # Slight transparency for glass effect
        self.root.configure(bg="#6054a4")  # Glow color background

        self.visible = True
        self.voice_enabled = True
        self.camera_on = False
        
        # Breathing animation variables
        self.breathing_active = False
        self.breathing_timer = None
        self.breathing_phase = 0

        # Position and sizing
        self.width = 420
        self.compact_height = 56
        self.expanded_height = 300
        self.is_expanded = False
        self.last_click_time = 0
        self.click_timer = None
        
        # Get screen dimensions for center-bottom positioning
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2  # Center horizontally
        y = screen_height - 110  # 110px from bottom
        
        # Start compact (add extra pixels for glow)
        self.root.geometry(f"{self.width + 8}x{self.compact_height + 8}+{x - 4}+{y - 4}")

        # Outer glow frame
        self.glow_frame = tk.Frame(self.root, bg="#6054a4")
        self.glow_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Main container with border effect
        self.main_frame = tk.Frame(self.glow_frame, bg="#0a0a0a", highlightthickness=1, highlightbackground="#1a3a4f")
        self.main_frame.pack(fill="both", expand=True)

        # Title frame with exit button - styled with gradient-like effect
        self.title_frame = tk.Frame(self.main_frame, bg="#0f1419", height=56)
        self.title_frame.pack(fill="x")
        self.title_frame.pack_propagate(False)
        
        # Exit button (X) - white icon on transparent background
        self.btn_exit = tk.Button(
            self.title_frame, text="✕",
            command=self.on_exit_click,
            bg="#0f1419", fg="#ffffff", relief="flat",
            font=("Segoe UI", 14, "bold"),
            padx=8, pady=4,
            activebackground="#0f1419", activeforeground="#ffffff",
            cursor="hand2",
            bd=0,
            highlightthickness=0
        )
        self.btn_exit.pack(side="left", padx=8, pady=4)
        
        # Add hover effect to exit button
        self.btn_exit.bind("<Enter>", lambda e: self.btn_exit.config(fg="#ffffff"))
        self.btn_exit.bind("<Leave>", lambda e: self.btn_exit.config(fg="#ffffff"))

        # Vertical separator
        separator1 = tk.Frame(self.title_frame, bg="#1a3a4f", width=1, height=30)
        separator1.pack(side="left", padx=2, pady=8, fill="y")

        # Title (always visible) - styled like dynamic island with glow
        self.title = tk.Label(
            self.title_frame, text="✨ Celestial AI",
            fg="#ffffff", bg="#0f1419",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2",
            padx=8,
            pady=8
        )
        self.title.pack(side="left", expand=True, fill="both")
        
        # Bind click event (will detect single vs double)
        self.title.bind("<Button-1>", self.on_title_click)
        # Bind motion for dragging
        self.title.bind("<B1-Motion>", self.do_move)
        self.btn_exit.bind("<B1-Motion>", self.do_move)

        # Content frame (will be shown/hidden) - dark glassmorphism style
        self.content_frame = tk.Frame(self.main_frame, bg="#0a0a0a")
        self.content_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Status with text wrapping - styled label with glow
        self.status = tk.Label(
            self.content_frame, text="Status: Listening",
            fg="#00ff88", bg="#0a0a0a",
            font=("Segoe UI", 9, "bold"),
            wraplength=350,
            justify="left",
            padx=5,
            pady=4
        )
        self.status.pack(pady=(4, 12), padx=5, fill="x")

        # Command entry - modern input field with border
        self.entry_frame = tk.Frame(self.content_frame, bg="#1a1a1a", highlightthickness=1, highlightbackground="#1a3a4f")
        self.entry_frame.pack(fill="x", padx=0, pady=(4, 10))
        
        self.entry = tk.Entry(
            self.entry_frame,
            bg="#0f1419",
            fg="#ffffff",
            insertbackground="#00ff88",
            relief="flat",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        self.entry.pack(fill="x", padx=8, pady=6)
        self.entry.bind("<Return>", self.submit_command)
        self.on_command_submit = None

        # Buttons frame for better layout with separator
        self.separator_line = tk.Frame(self.content_frame, bg="#1a3a4f", height=1)
        self.separator_line.pack(fill="x", pady=4)
        
        self.buttons_frame = tk.Frame(self.content_frame, bg="#0a0a0a")
        self.buttons_frame.pack(fill="x", pady=(4, 0))

        # Buttons - modern minimal style with borders
        self.btn_voice = tk.Button(
            self.buttons_frame, text="🎤 Voice",
            command=self.toggle_voice,
            bg="#1a1a1a", fg="#00ff88", relief="flat",
            font=("Segoe UI", 8, "bold"),
            padx=10, pady=6,
            activebackground="#0f1419", activeforeground="#00ff88",
            cursor="hand2",
            bd=1,
            highlightthickness=0
        )
        self.btn_voice.pack(side="left", padx=3, expand=True, fill="x")
        
        # Hover effects for voice button - purple on hover, green otherwise
        self.btn_voice.bind("<Enter>", lambda e: self.btn_voice.config(bg="#252525", fg="#6054a4"))
        self.btn_voice.bind("<Leave>", lambda e: self.btn_voice.config(bg="#1a1a1a", fg="#00ff88"))
        self.btn_voice.bind("<Button-1>", lambda e: self.btn_voice.config(fg="#00ff88"))

        self.btn_camera = tk.Button(
            self.buttons_frame, text="📷 Camera",
            command=self.toggle_camera,
            bg="#1a1a1a", fg="#00ff88", relief="flat",
            font=("Segoe UI", 8, "bold"),
            padx=10, pady=6,
            activebackground="#0f1419", activeforeground="#00ff88",
            cursor="hand2",
            bd=1,
            highlightthickness=0
        )
        self.btn_camera.pack(side="left", padx=3, expand=True, fill="x")
        
        # Hover effects for camera button - purple on hover, green otherwise
        self.btn_camera.bind("<Enter>", lambda e: self.btn_camera.config(bg="#252525", fg="#6054a4"))
        self.btn_camera.bind("<Leave>", lambda e: self.btn_camera.config(bg="#1a1a1a", fg="#00ff88"))
        self.btn_camera.bind("<Button-1>", lambda e: self.btn_camera.config(fg="#00ff88"))

        # Initially hide content (but keep frame created)
        self.content_frame.pack(fill="both", expand=True, padx=12, pady=12)
        self.content_frame.pack_forget()

        # Drag support variables
        self.x_offset = 0
        self.y_offset = 0

        # Callbacks (set by core)
        self.on_voice_toggle = None
        self.on_camera_toggle = None
        self.on_exit_requested = None
        
        # Ensure window is visible
        self.root.update()
        
        # Start breathing animation since initial status is "Listening"
        self.start_breathing()

    def on_exit_click(self):
        """Handle exit button click - submit 'exit' command"""
        if self.on_command_submit:
            self.on_command_submit("exit")

    def start_breathing(self):
        """Start the breathing animation for status"""
        if self.breathing_active:
            return
        self.breathing_active = True
        self.breathing_phase = 0
        self.animate_breathing()

    def stop_breathing(self):
        """Stop the breathing animation"""
        self.breathing_active = False
        if self.breathing_timer:
            self.root.after_cancel(self.breathing_timer)
            self.breathing_timer = None

    def animate_breathing(self):
        """Animate breathing effect on the UI panel - hover effect when collapsed"""
        if not self.breathing_active or self.is_expanded:
            # Stop breathing if panel is expanded
            return
        
        try:
            # Breathing scale: slightly expand and contract the height
            # Creates a gentle hovering/pulsing effect
            min_height = self.compact_height
            max_height = self.compact_height + 8  # Hover effect
            
            # Smooth breathing cycle
            cycle = (self.breathing_phase % 20) / 10.0  # 0 to 2, repeats every 20 phases
            if cycle < 1:
                # Expansion phase
                height = int(min_height + (max_height - min_height) * cycle)
            else:
                # Contraction phase
                height = int(max_height - (max_height - min_height) * (cycle - 1))
            
            # Get current geometry
            geom = self.root.geometry()
            parts = geom.split('+')
            width_part = parts[0].split('x')
            width = int(width_part[0])
            x = parts[1] if len(parts) > 1 else '20'
            y = parts[2] if len(parts) > 2 else '200'
            
            # Update with new height
            self.root.geometry(f"{self.width + 8}x{height + 8}+{x}+{y}")
            
            self.breathing_phase = (self.breathing_phase + 1) % 20
            self.breathing_timer = self.root.after(100, self.animate_breathing)
        except Exception as e:
            # Silently handle errors to prevent UI from breaking
            print(f"Breathing animation error: {e}")
            self.breathing_active = False

    def start_move(self, e):
        """Prepare for dragging"""
        self.x_offset = e.x
        self.y_offset = e.y

    def on_title_click(self, event):
        """Handle click - single for drag, double for expand/collapse"""
        self.x_offset = event.x
        self.y_offset = event.y
        
        # Cancel previous timer if exists
        if self.click_timer:
            self.root.after_cancel(self.click_timer)
            self.click_timer = None
            # This was a double-click
            self.toggle_expand(event)
        else:
            # Schedule to check if second click comes (for double-click detection)
            self.click_timer = self.root.after(250, self.single_click_handler)

    def single_click_handler(self):
        """Called if no second click within 250ms - this is a single click for dragging"""
        self.click_timer = None
        # Single click was confirmed, but we already captured x_offset and y_offset
        # The B1-Motion binding will handle the drag

    def do_move(self, e):
        x = self.root.winfo_pointerx() - self.x_offset
        y = self.root.winfo_pointery() - self.y_offset
        self.root.geometry(f"+{x}+{y}")

    def toggle_expand(self, event=None):
        """Toggle expand/collapse on double-click"""
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        """Expand the panel with animation"""
        if self.is_expanded:
            return
        self.is_expanded = True
        self.stop_breathing()  # Stop breathing when expanded
        self.content_frame.pack(fill="both", expand=True, padx=12, pady=12)
        self.animate_height(self.compact_height, self.expanded_height)

    def collapse(self):
        """Collapse the panel with animation"""
        if not self.is_expanded:
            return
        self.is_expanded = False
        self.animate_height(self.expanded_height, self.compact_height)
        self.root.after(150, lambda: self.content_frame.pack_forget())
        self.root.after(200, self.start_breathing)  # Start breathing after collapse animation

    def animate_height(self, start, end):
        """Animate height change"""
        step = 10 if end > start else -10
        current = start
        while (step > 0 and current < end) or (step < 0 and current > end):
            current += step
            self.root.geometry(f"{self.width + 8}x{current + 8}")
            self.root.update()
            self.root.after(5)
        # Final geometry
        self.root.geometry(f"{self.width + 8}x{end + 8}")

    def submit_command(self, event):
        text = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if text and self.on_command_submit:
            self.on_command_submit(text)

    def set_status(self, text):
        self.status.config(text=f"Status: {text}")

    def toggle(self):
        self.root.withdraw() if self.visible else self.root.deiconify()
        self.visible = not self.visible

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled
        status_text = "ON" if self.voice_enabled else "OFF"
        self.btn_voice.config(text=f"🎤 Voice: {status_text}")
        if self.on_voice_toggle:
            self.on_voice_toggle(self.voice_enabled)

    def toggle_camera(self):
        self.camera_on = not self.camera_on
        status_text = "ON" if self.camera_on else "OFF"
        self.btn_camera.config(text=f"📷 Camera: {status_text}")
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

