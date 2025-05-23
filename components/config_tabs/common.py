import tkinter as tk
from tkinter import ttk

# Try importing colors, falling back to a default set if not available
try:
    from utils.ui_components import COLORS, ModernButton
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

def create_name_textbox(parent, label_text="Name(Use):"):
    """Create a standardized name textbox with label."""
    frame = tk.Frame(parent, bg=COLORS["bg_medium"])
    frame.pack(pady=2, fill="x")
    
    label = tk.Label(
        frame, 
        text=label_text, 
        bg=COLORS["bg_medium"], 
        fg=COLORS["accent"], 
        font=("Segoe UI", 11)
    )
    label.pack(pady=0)
    
    # Create a nicer looking textbox with rounded corners (simulation)
    text_frame = tk.Frame(frame, bg=COLORS["bg_light"], bd=0, highlightthickness=1, 
                       highlightbackground=COLORS["selection"], highlightcolor=COLORS["accent"])
    text_frame.pack(pady=1, fill="x", padx=10)
    
    textbox = tk.Text(
        text_frame, 
        height=1.2, 
        width=30, 
        wrap="word", 
        bg=COLORS["bg_light"], 
        fg=COLORS["text"], 
        font=("Segoe UI", 10),
        bd=0,
        padx=5,
        pady=2,
        insertbackground=COLORS["accent"]  # Cursor color
    )
    textbox.pack(pady=1, fill="x", padx=1, expand=True)
    
    return textbox

def create_save_button(parent, command, text="Save"):
    """Create a standardized save button with curved corners."""
    # Create a frame to hold the button for consistent positioning
    button_frame = tk.Frame(parent, bg=parent["bg"] if isinstance(parent, tk.Frame) else COLORS["bg_medium"])
    
    # Create a custom Canvas button with rounded corners for better visibility
    canvas_width = 100  # Total width
    canvas_height = 36  # Total height
    corner_radius = 10  # Rounded corner radius
    
    button_canvas = tk.Canvas(
        button_frame,
        width=canvas_width,
        height=canvas_height,
        bg=parent["bg"] if isinstance(parent, tk.Frame) else COLORS["bg_medium"],
        highlightthickness=0,
        cursor="hand2"
    )
    button_canvas.pack(pady=5, padx=5)
    
    # Function to create a rounded rectangle
    def create_rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    # Create button background with rounded corners
    button_bg = create_rounded_rect(
        button_canvas, 
        2, 2, 
        canvas_width-2, canvas_height-2, 
        corner_radius, 
        fill=COLORS["accent"],
        outline=""
    )
    
    # Create text on button
    button_text = button_canvas.create_text(
        canvas_width/2, 
        canvas_height/2, 
        text=text,
        fill=COLORS["bg_dark"],
        font=("Segoe UI", 10, "bold")
    )
    
    # Store the initial colors for state changes
    button_canvas.normal_bg = COLORS["accent"]
    button_canvas.normal_fg = COLORS["bg_dark"]
    button_canvas.hover_bg = COLORS["selection"]
    button_canvas.hover_fg = COLORS["text"]
    button_canvas.disabled_bg = COLORS["bg_light"]
    button_canvas.disabled_fg = COLORS["text_dim"]
    
    # Create a state variable for the button
    button_canvas.state = "disabled"  # Start as disabled
    
    # Create the button interface methods
    def set_state(state):
        button_canvas.state = state
        if state == "normal":
            button_canvas.itemconfig(button_bg, fill=button_canvas.normal_bg)
            button_canvas.itemconfig(button_text, fill=button_canvas.normal_fg)
        elif state == "disabled":
            button_canvas.itemconfig(button_bg, fill=button_canvas.disabled_bg)
            button_canvas.itemconfig(button_text, fill=button_canvas.disabled_fg)
    
    def get_state():
        return button_canvas.state
    
    # Button hover effects
    def on_enter(event):
        if button_canvas.state != "disabled":
            button_canvas.itemconfig(button_bg, fill=button_canvas.hover_bg)
            button_canvas.itemconfig(button_text, fill=button_canvas.hover_fg)
    
    def on_leave(event):
        if button_canvas.state != "disabled":
            button_canvas.itemconfig(button_bg, fill=button_canvas.normal_bg)
            button_canvas.itemconfig(button_text, fill=button_canvas.normal_fg)
    
    def on_click(event):
        if button_canvas.state != "disabled":
            if command:
                command()
    
    # Bind events
    button_canvas.bind("<Enter>", on_enter)
    button_canvas.bind("<Leave>", on_leave)
    button_canvas.bind("<Button-1>", on_click)
    
    # Add necessary methods to mimic a button
    button_canvas.config = lambda **kwargs: None  # Dummy config method
    button_canvas.configure = button_canvas.config
    
    # Add state methods
    button_canvas.set_state = set_state
    button_canvas.cget = lambda key: button_canvas.state if key == "state" else None
    
    # Initial state
    set_state("disabled")
    
    # Store the button as an attribute of the frame for easy access
    button_frame.button = button_canvas
    
    return button_frame
