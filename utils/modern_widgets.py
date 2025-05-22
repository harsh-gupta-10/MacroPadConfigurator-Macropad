import tkinter as tk

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

# Enhanced Modern Key Button class with improved hover effects
class ModernKeyButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, width=100, height=80, corner_radius=10, **kwargs):
        # Extract custom properties but allow them to be overridden
        bg_color = kwargs.pop('bg', COLORS["bg_light"]) if 'bg' in kwargs else COLORS["bg_light"]
        fg_color = kwargs.pop('fg', COLORS["text"]) if 'fg' in kwargs else COLORS["text"]
        hover_bg = kwargs.pop('activebg', COLORS["accent"]) if 'activebg' in kwargs else COLORS["accent"]
        hover_fg = kwargs.pop('activefg', COLORS["bg_dark"]) if 'activefg' in kwargs else COLORS["bg_dark"]
        
        # Use the extracted bg_color for the background
        super().__init__(
            parent, 
            width=width, 
            height=height, 
            highlightthickness=0, 
            bg=COLORS["bg_medium"],
            **kwargs
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
            font=("Segoe UI", 9, "bold"),
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
            x1, y1        ]
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
        else:            # Just set the name if there's no key combo
            self.itemconfig(self.name_id, text=text)
            self.itemconfig(self.keys_id, text="")

    def set_profile_text(self, text):
        """Set text for a profile button - positioned in the center without splitting"""
        # Update text position to center of button with a smaller font for better fit
        self.itemconfig(self.name_id, text=text, font=("Segoe UI", 10, "bold"))  # Reduced from 12 to 10
        self.itemconfig(self.keys_id, text="")  # Clear any key text
        
        # Adjust position of main text to center
        self.coords(self.name_id, self.width/2, self.height/2)

    def set_selected(self, selected):
        """Set the selected state of this button with enhanced visual feedback"""
        self.selected = selected
        if selected:
            # Create an enhanced glowing border effect
            self.itemconfig(self.rect_id, fill=COLORS["selection"])
            # Make text more prominent with accent color
            self.itemconfig(self.name_id, fill=COLORS["accent"])
            self.itemconfig(self.keys_id, fill=COLORS["accent"])
            # Make the font bolder but smaller when selected
            self.itemconfig(self.name_id, font=("Segoe UI", 10, "bold"))
            # Add a shadow effect for depth
            self.itemconfig(self.shadow_id, fill=COLORS["accent"])
        else:
            # Reset to normal state
            self.itemconfig(self.rect_id, fill=self.bg_color)
            self.itemconfig(self.name_id, fill=self.fg_color)
            self.itemconfig(self.keys_id, fill=self.fg_color)
            # Reset font to normal and smaller
            self.itemconfig(self.name_id, font=("Segoe UI", 9, "bold"))
            # Reset shadow
            self.itemconfig(self.shadow_id, fill="#222222")
    
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

