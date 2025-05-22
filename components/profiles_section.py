# filepath: d:\codes2\pico pad\MacroPadConfigurator\components\profiles_section.py
import tkinter as tk
from engine import load_profiles

# Define colors directly to avoid circular imports
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

# Import custom widgets and UI components
from utils.ui_components import ModernFrame
from utils.modern_widgets import ModernKeyButton

class ProfilesSection:
    def __init__(self, root, app=None):
        self.root = root
        self.app = app  # Reference to main app
        
        # Create modern frame with curved corners
        if "ModernFrame" in globals():
            self.profile_frame = ModernFrame(
                self.root, 
                corner_radius=15, 
                padding=10,
                bg=COLORS["bg_medium"]
            )
        else:
            self.profile_frame = tk.Frame(self.root, bg=COLORS["bg_medium"], bd=2, relief="ridge")
            
        # Increased width to prevent profile names from being cut off
        self.profile_frame.place(x=10, y=10, width=185, height=430)
        
        # Get interior frame reference
        interior = self.profile_frame.interior if hasattr(self.profile_frame, "interior") else self.profile_frame
        
        # Title with modern styling - reduced font size
        title_frame = tk.Frame(interior, bg=COLORS["bg_medium"])
        title_frame.pack(fill="x", pady=(0, 2))
        
        title_label = tk.Label(
            title_frame, 
            text="Profiles", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"], 
            font=("Segoe UI", 14, "bold")  # Reduced from 16 to 14
        )
        title_label.pack(side="left", padx=10)
        
        # Add a subtle separator line
        separator = tk.Frame(interior, height=1, bg=COLORS["bg_light"])
        separator.pack(fill="x", padx=5, pady=1)
        
        # Create a container frame for the profile buttons
        self.button_container = tk.Frame(interior, bg=COLORS["bg_medium"])
        self.button_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.profile_buttons = []
        profiles = load_profiles()
        profile_names = {
            "0": "Default", 
            "1": "VSCode", 
            "2": "OBS", 
            "3": "Software", 
            "4": "Windows", 
            "5": "Photoshop"
        }
        
        # Track the first profile to select by default
        first_profile = None
        
        # Create modern buttons for profiles
        for profile_id in sorted(profiles.keys()):
            name = profile_names.get(profile_id, f"Profile {profile_id}")
            
            # Save the first profile ID for default selection
            if first_profile is None:
                first_profile = profile_id
            
            # If ModernKeyButton is available, use it for consistency with keypad
            if "ModernKeyButton" in globals():
                btn = ModernKeyButton(
                    self.button_container,
                    text=name,
                    command=lambda p=profile_id: self.select_profile(p),
                    width=170,  # Wider to ensure profile names are fully visible
                    height=40,  # Shorter height for profile buttons
                    corner_radius=10,
                    bg=COLORS["bg_light"],
                    fg=COLORS["text"],
                    activebg=COLORS["accent"],
                    activefg=COLORS["bg_dark"]
                )
                # Use the dedicated profile text method with smaller font
                btn.set_profile_text(name)
                btn.pack(pady=4)
                self.profile_buttons.append((profile_id, btn))
            else:
                # Fallback to standard button with improved styling
                btn = tk.Button(
                    self.button_container, 
                    text=name, 
                    bg=COLORS["bg_light"],
                    fg=COLORS["text"], 
                    relief="flat",
                    font=("Segoe UI", 9, "bold"),  # Smaller font size
                    activebackground=COLORS["accent"], 
                    activeforeground=COLORS["bg_dark"],
                    command=lambda p=profile_id: self.select_profile(p)
                )
                btn.pack(fill="x", padx=5, pady=4)
                self.profile_buttons.append((profile_id, btn))
        
        # Select the first profile by default after short delay to ensure UI is ready
        if first_profile is not None and self.app:
            self.root.after(100, lambda: self.select_profile(first_profile))

    def select_profile(self, profile):
        """Handle profile selection."""
        # Update button appearance
        for profile_id, btn in self.profile_buttons:
            is_selected = profile_id == profile
            
            if "ModernKeyButton" in globals() and isinstance(btn, ModernKeyButton):
                # For ModernKeyButton, set the selected state and enhance appearance
                btn.set_selected(is_selected)
                
                # Enhanced visual cues for selected profile
                if is_selected:
                    # Add stronger glow effect with accent color
                    btn.itemconfig(btn.shadow_id, fill=COLORS["accent"])  # More visible accent
                    # Change background to selection color
                    btn.itemconfig(btn.rect_id, fill=COLORS["selection"])
                    # Add a border effect for more emphasis (if supported)
                    try:
                        btn.itemconfig(btn.rect_id, outline=COLORS["accent"], width=2)
                    except tk.TclError:
                        # Outline not supported, use other visual cues
                        pass
                else:
                    # Reset shadow to normal
                    btn.itemconfig(btn.shadow_id, fill="#222222")
                    # Reset background color
                    btn.itemconfig(btn.rect_id, fill=COLORS["bg_light"])
                    # Remove outline if supported
                    try:
                        btn.itemconfig(btn.rect_id, outline="")
                    except tk.TclError:
                        pass
            else:
                # For standard buttons, update colors and add border for better visibility
                if is_selected:
                    btn.config(
                        bg=COLORS["accent"],
                        fg=COLORS["bg_dark"],
                        relief="solid",
                        bd=2,
                        highlightbackground=COLORS["text"],
                        highlightthickness=1
                    )
                else:
                    btn.config(
                        bg=COLORS["bg_light"],
                        fg=COLORS["text"],
                        relief="flat", 
                        bd=0,
                        highlightthickness=0
                    )
                
        # Update the app's selected profile
        if self.app:
            self.app.set_selected_profile(profile)
