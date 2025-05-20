import tkinter as tk
from engine import load_profiles

# Import our custom widgets
from utils.modern_widgets import ModernKeyButton

# Import colors and UI components
try:
    from main import COLORS
    from utils.ui_components import ModernFrame
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

class KeypadSection:
    def __init__(self, root, app=None):
        self.root = root
        self.app = app  # Reference to main app
        self.selected_key = None
        
        # Create modern frame with curved corners
        if 'ModernFrame' in globals():
            self.keypad_frame = ModernFrame(
                self.root, 
                corner_radius=15, 
                padding=10,
                bg=COLORS["bg_medium"]
            )
        else:
            self.keypad_frame = tk.Frame(self.root, bg=COLORS["bg_medium"], bd=2, relief="ridge")
            
        self.keypad_frame.place(x=200, y=70, width=350, height=370)
        
        # Get interior frame reference
        interior = self.keypad_frame.interior if hasattr(self.keypad_frame, 'interior') else self.keypad_frame
        
        # Title with modern styling
        title_frame = tk.Frame(interior, bg=COLORS["bg_medium"])
        title_frame.pack(fill="x", pady=(5, 15))
        
        title_label = tk.Label(
            title_frame, 
            text="Keypad", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"], 
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Add a subtle separator line
        separator = tk.Frame(interior, height=1, bg=COLORS["bg_light"])
        separator.pack(fill="x", padx=20, pady=5)
        
        # Frame for keypad grid with a slight gradient background
        self.button_frame = tk.Frame(interior, bg=COLORS["bg_medium"])
        self.button_frame.pack(expand=True)
        
        self.key_buttons = []
        self.create_keypad()
        
        # Initialize with default profile if available
        if self.app and hasattr(self.app, 'selected_profile'):
            self.update_keys(self.app.selected_profile)

    def create_keypad(self):
        """Create the keypad buttons."""
        # Clear any existing buttons
        for button in self.key_buttons:
            button[1].destroy()
        self.key_buttons = []
        
        # Create new buttons with modern styling
        for i in range(9):
            key_num = str(i + 1)
            
            # Use modern button class
            btn = ModernKeyButton(
                self.button_frame,
                text=f"Key {key_num}",
                command=lambda k=key_num: self.configure_key(k),
                width=100,
                height=80,
                corner_radius=12,
                bg=COLORS["bg_light"],
                fg=COLORS["text"],
                activebg=COLORS["accent"],
                activefg=COLORS["bg_dark"]
            )
            
            # Position button in grid with slightly more space
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.key_buttons.append((key_num, btn))

    def update_keys(self, profile_id):
        """Update keypad buttons with the selected profile's configuration."""
        profiles = load_profiles()
        
        if profile_id not in profiles:
            print(f"Profile {profile_id} not found")
            return
            
        profile = profiles[profile_id]
        
        for key_num, btn in self.key_buttons:
            if key_num in profile:
                key_config = profile[key_num]
                name = key_config.get("name", f"Key {key_num}")
                keys = key_config.get("key", [])
                  # Format button text based on key type
                if "text_type" in key_config:
                    # This is a text input key
                    text_type = key_config.get("text_type")
                    if text_type == "single":
                        display_text = "Single Line Text"
                    else:
                        display_text = "Paragraph Text"
                    btn.set_text(f"{name}\n[{display_text}]")
                # Check if this key has software assigned
                elif "software" in key_config:
                    # Add software indicator by adjusting the text
                    software_name = key_config["software"].split("\\")[-1].split(".")[0]
                    btn.set_text(f"{name}\n[Launch: {software_name}]")
                # Normal key combination
                elif keys:
                    key_text = f"{name}\n[{' + '.join(keys)}]"
                    btn.set_text(key_text)
                else:
                    # No special configuration
                    btn.set_text(name)
            else:
                btn.set_text(f"Key {key_num}\n[Not Set]")
                
        # Reset selected status if needed
        if self.selected_key:
            self.configure_key(self.selected_key, update_app=False)

    def configure_key(self, key, update_app=True):
        """Handle key configuration."""
        self.selected_key = key
        
        # Update selected state for all buttons
        for key_num, btn in self.key_buttons:
            btn.set_selected(key_num == key)
            
        # Update app's selected key if needed
        if update_app and self.app and hasattr(self.app, 'set_selected_key'):
            self.app.set_selected_key(key)