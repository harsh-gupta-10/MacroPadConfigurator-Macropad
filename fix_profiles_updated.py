import tkinter as tk
from engine import load_profiles

# Import custom widgets and UI components
try:
    # Avoiding circular import by not importing from main
    from utils.ui_components import ModernFrame
    from utils.modern_widgets import ModernKeyButton
    # Define colors locally to avoid circular import
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
    
    # Use ModernFrame from our ui_components module
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
            
        self.profile_frame.place(x=10, y=10, width=200, height=430)
        
        # Get interior frame reference
        interior = self.profile_frame.interior if hasattr(self.profile_frame, "interior") else self.profile_frame
        
        # Title with modern styling
        title_frame = tk.Frame(interior, bg=COLORS["bg_medium"])
        title_frame.pack(fill="x", pady=(0, 2))
        
        title_label = tk.Label(
            title_frame, 
            text="Profiles", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"], 
            font=("Segoe UI", 16, "bold")
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
        
        # Create modern buttons for profiles
        for profile_id in sorted(profiles.keys()):
            name = profile_names.get(profile_id, f"Profile {profile_id}")
            
            # If ModernKeyButton is available, use it for consistency with keypad
            if "ModernKeyButton" in globals():
                btn = ModernKeyButton(
                    self.button_container,
                    text=name,
                    command=lambda p=profile_id: self.select_profile(p),
                    width=160,  # Slightly narrower than the frame
                    height=40,  # Shorter height for profile buttons
                    corner_radius=20,
                    bg=COLORS["bg_light"],
                    fg=COLORS["text"],
                    activebg=COLORS["accent"],
                    activefg=COLORS["bg_dark"]
                )
                # Use the dedicated profile text method
                btn.set_profile_text(name)
                btn.pack(pady=4)
            else:
                # Fallback to standard button with improved styling
                btn = tk.Button(
                    self.button_container, 
                    text=name, 
                    bg=COLORS["bg_light"],
                    fg=COLORS["text"], 
                    relief="flat",
                    font=("Segoe UI", 10, "bold"), 
                    activebackground=COLORS["accent"], 
                    activeforeground=COLORS["bg_dark"],
                    command=lambda p=profile_id: self.select_profile(p)
                )
                btn.pack(fill="x", padx=5, pady=4)
                
            self.profile_buttons.append((profile_id, btn))

    def select_profile(self, profile):
        """Handle profile selection."""
        # Update button appearance
        for profile_id, btn in self.profile_buttons:
            if "ModernKeyButton" in globals() and isinstance(btn, ModernKeyButton):
                # For ModernKeyButton, set the selected state and enhance appearance
                is_selected = profile_id == profile
                btn.set_selected(is_selected)
                
                # Additional visual cues for selected profile
                if is_selected:
                    # Add glow effect with accent color
                    btn.itemconfig(btn.shadow_id, fill=COLORS["accent"] + "80")  # Semi-transparent accent
                else:
                    # Reset shadow to normal
                    btn.itemconfig(btn.shadow_id, fill="#222222")
            else:
                # For standard buttons, update colors
                if profile_id == profile:
                    btn.config(bg=COLORS["accent"], fg=COLORS["bg_dark"])
                else:
                    btn.config(bg=COLORS["bg_light"], fg=COLORS["text"])
                
        # Update the app's selected profile
        if self.app:
            self.app.set_selected_profile(profile)
