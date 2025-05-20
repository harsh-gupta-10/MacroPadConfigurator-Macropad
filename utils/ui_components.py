import tkinter as tk

# Try importing colors, falling back to a default set if not available
try:
    from main import COLORS
except ImportError:
    # Fallback colors - modern dark theme
    COLORS = {
        "bg_dark": "#1E1E2E",     # Dark background
        "bg_medium": "#2A2A3C",   # Medium background for frames
        "bg_light": "#313244",    # Light background for elements
        "accent": "#89B4FA",      # Blue accent color
        "text": "#CDD6F4",        # Light text
        "text_dim": "#A6ADC8",    # Dimmed text
        "success": "#A6E3A1",     # Green for success
        "warning": "#F9E2AF",     # Yellow for warnings
        "error": "#F38BA8",       # Red for errors
        "selection": "#45475A"    # Selection color
    }

class ModernFrame(tk.Frame):
    """A modern-looking frame with rounded corners and optional padding."""
    def __init__(self, parent, corner_radius=10, padding=5, **kwargs):
        # Extract bg from kwargs or use default
        bg = kwargs.pop('bg', COLORS["bg_medium"])
        
        # Create outer frame
        super().__init__(parent, bg=bg, highlightthickness=0, **kwargs)
        
        # Create interior frame with padding
        self.interior = tk.Frame(self, bg=bg, padx=padding, pady=padding)
        self.interior.pack(fill='both', expand=True)
        
        # Store parameters
        self.corner_radius = corner_radius
        self.bg = bg
        
        # Bind redraw event
        self.bind('<Configure>', self._on_resize)
        
    def _on_resize(self, event):
        # This could be expanded to redraw rounded corners with a canvas
        # For now we're keeping it simple
        pass

class ModernTitle(tk.Frame):
    """A modern title section with an accent line."""
    def __init__(self, parent, title_text, **kwargs):
        bg = kwargs.pop('bg', COLORS["bg_medium"])
        fg = kwargs.pop('fg', COLORS["accent"])
        font = kwargs.pop('font', ("Segoe UI", 16, "bold"))
        
        super().__init__(parent, bg=bg, **kwargs)
        
        # Create title label
        self.title = tk.Label(
            self, 
            text=title_text, 
            bg=bg, 
            fg=fg, 
            font=font
        )
        self.title.pack(side="left", padx=10, pady=(5, 0))
        
        # Add a subtle separator line
        self.separator = tk.Frame(parent, height=1, bg=COLORS["bg_light"])
        self.separator.pack(fill="x", padx=20, pady=5)

class ModernButton(tk.Button):
    """A modern styled button with hover effects."""
    
    def __init__(self, parent, **kwargs):
        # Set default styling
        kwargs['bg'] = kwargs.get('bg', COLORS["bg_light"])
        kwargs['fg'] = kwargs.get('fg', COLORS["text"])
        kwargs['activebackground'] = kwargs.get('activebackground', COLORS["accent"])
        kwargs['activeforeground'] = kwargs.get('activeforeground', COLORS["bg_dark"])
        kwargs['relief'] = kwargs.get('relief', tk.FLAT)
        kwargs['borderwidth'] = kwargs.get('borderwidth', 0)
        kwargs['padx'] = kwargs.get('padx', 10)
        kwargs['pady'] = kwargs.get('pady', 5)
        kwargs['font'] = kwargs.get('font', ("Segoe UI", 10))
        
        super().__init__(parent, **kwargs)
        
        # Add hover effect
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, e):
        if self['state'] != tk.DISABLED:
            self.config(bg=COLORS["selection"])
    
    def _on_leave(self, e):
        if self['state'] != tk.DISABLED:
            self.config(bg=COLORS["bg_light"])

# More UI components can be added here as needed
