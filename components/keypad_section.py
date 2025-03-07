import tkinter as tk
from engine import load_profiles

# Import colors and ModernFrame if available
try:
    from main import COLORS, ModernFrame
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
    
    # Simple ModernFrame implementation as before

# Enhanced Modern Key Button class with improved hover effects
class ModernKeyButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, width=100, height=80, corner_radius=10, **kwargs):
        bg_color = kwargs.get('bg', COLORS["bg_light"])
        fg_color = kwargs.get('fg', COLORS["text"])
        hover_bg = kwargs.get('activebg', COLORS["accent"])
        hover_fg = kwargs.get('activefg', COLORS["bg_dark"])
        
        super().__init__(
            parent, 
            width=width, 
            height=height, 
            highlightthickness=0, 
            bg=COLORS["bg_medium"]
        )
        
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_bg = hover_bg
        self.hover_fg = hover_fg
        self.command = command
        self.hovered = False
        self.selected = False
        self.width = width
        self.height = height
        
        # Create shadow for depth effect - using solid colors instead of alpha
        self.shadow_id = self.create_rounded_rect(
            8, 8, width-2, height-2, 
            corner_radius, 
            fill="#222222",  # Dark gray for shadow (instead of #00000030)
            outline=""
        )
        
        # Create rounded rectangle for button background
        self.rect_id = self.create_rounded_rect(
            5, 5, width-5, height-5, 
            corner_radius, 
            fill=self.bg_color, 
            outline=""
        )
        
        # Create separate text elements for name and keys
        self.name_id = self.create_text(
            width/2, height/2 - 15, 
            text=text, 
            fill=self.fg_color, 
            font=("Segoe UI", 10, "bold"),
            width=width-20,
            justify="center"
        )
        
        self.keys_id = self.create_text(
            width/2, height/2 + 15, 
            text="", 
            fill=self.fg_color, 
            font=("Segoe UI", 8),
            width=width-20,
            justify="center"
        )
        
        # Add a subtle highlight on the top edge for 3D effect - using solid color
        self.highlight_id = self.create_line(
            5 + corner_radius, 7, 
            width - 5 - corner_radius, 7, 
            fill="#444444",  # Light gray for highlight (instead of #ffffff20)
            width=1.5
        )
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        # Create a rounded rectangle as before
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
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def set_text(self, text):
        # Parse the text to separate name and keys
        if "\n[" in text:
            name, keys = text.split("\n[", 1)
            keys = keys.rstrip("]")
            self.itemconfig(self.name_id, text=name)
            
            # Format the keys with a nice symbol
            if keys == "Not Set":
                self.itemconfig(self.keys_id, text="◇ Not Set")
            else:
                self.itemconfig(self.keys_id, text="◆ " + keys)
        else:
            # Just set the name if there's no key combo
            self.itemconfig(self.name_id, text=text)
            self.itemconfig(self.keys_id, text="")
    
    def set_selected(self, selected):
        """Set the selected state of this button"""
        self.selected = selected
        if selected:
            # Create a glowing border effect
            self.itemconfig(self.rect_id, fill=COLORS["selection"])
            self.itemconfig(self.name_id, fill=COLORS["accent"])
            self.itemconfig(self.keys_id, fill=COLORS["accent"])
        else:
            # Reset to normal state
            self.itemconfig(self.rect_id, fill=self.bg_color)
            self.itemconfig(self.name_id, fill=self.fg_color)
            self.itemconfig(self.keys_id, fill=self.fg_color)
    
    def on_enter(self, event):
        """Handle mouse enter event with smoother hover effect"""
        if not self.hovered and not self.selected:
            # Change background and text colors
            self.itemconfig(self.rect_id, fill=self.hover_bg)
            self.itemconfig(self.name_id, fill=self.hover_fg)
            self.itemconfig(self.keys_id, fill=self.hover_fg)
            
            # Instead of moving the button (which causes artifacts),
            # just darken the shadow slightly for a pressed effect
            self.itemconfig(self.shadow_id, fill="#111111")  # Darker shadow on hover
            
            self.hovered = True
    
    def on_leave(self, event):
        """Handle mouse leave event"""
        if self.hovered and not self.selected:
            # Reset colors
            self.itemconfig(self.rect_id, fill=self.bg_color)
            self.itemconfig(self.name_id, fill=self.fg_color)
            self.itemconfig(self.keys_id, fill=self.fg_color)
            
            # Reset shadow
            self.itemconfig(self.shadow_id, fill="#222222")  # Normal shadow
            
            self.hovered = False
    
    def on_click(self, event):
        """Handle click with proper visual feedback"""
        # Store the command to execute later
        self._pending_command = self.command if self.hovered else None
        
        # Flash effect with text color change
        self.itemconfig(self.rect_id, fill=COLORS["accent"])
        self.itemconfig(self.shadow_id, fill="#000000")  # Very dark shadow when clicked
        self.itemconfig(self.name_id, fill=COLORS["bg_dark"])  # Change text color too
        self.itemconfig(self.keys_id, fill=COLORS["bg_dark"])  # Change text color too
        
        # Schedule return to previous state
        self.after(100, self._restore_after_click)

    def _restore_after_click(self):
        """Restore button appearance after click"""
        # Restore background based on state
        if self.selected:
            self.itemconfig(self.rect_id, fill=COLORS["selection"])
            self.itemconfig(self.name_id, fill=COLORS["accent"])
            self.itemconfig(self.keys_id, fill=COLORS["accent"])
        elif self.hovered:
            self.itemconfig(self.rect_id, fill=self.hover_bg)
            self.itemconfig(self.name_id, fill=self.hover_fg)
            self.itemconfig(self.keys_id, fill=self.hover_fg)
        else:
            self.itemconfig(self.rect_id, fill=self.bg_color)
            self.itemconfig(self.name_id, fill=self.fg_color)
            self.itemconfig(self.keys_id, fill=self.fg_color)
        
        # Restore shadow
        self.itemconfig(self.shadow_id, fill="#111111" if self.hovered else "#222222")

    def on_release(self, event):
        """Handle mouse button release"""
        # Execute the stored command if it exists
        if hasattr(self, '_pending_command') and self._pending_command:
            self._pending_command()
            delattr(self, '_pending_command')

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
                
                # Format button text in a more visually appealing way
                if keys:
                    key_text = f"{name}\n[{' + '.join(keys)}]"
                else:
                    key_text = name
                    
                btn.set_text(key_text)
                
                # Check if this key has software assigned
                if "software" in key_config:
                    # Add software indicator by adjusting the text
                    software_name = key_config["software"].split("\\")[-1].split(".")[0]
                    btn.set_text(f"{name}\n[Launch: {software_name}]")
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