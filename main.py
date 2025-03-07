import tkinter as tk

from components.profiles_section import ProfilesSection
from components.keypad_section import KeypadSection
from components.config_panel import ConfigPanel
from components.status_bar import StatusBar
from engine import load_profiles

class MacroPadConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("MacroPad Configurator")
        self.root.geometry("900x500")
        self.root.configure(bg="black")
        
        # Track selected profile and key
        self.selected_profile = "0"  # Default profile
        self.selected_key = None
        
        # Create UI layout
        self.create_ui()
        
        # Set up window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        """Create the main UI layout."""
        # Top Options Section
       
        # Profiles section
        self.profiles_section = ProfilesSection(self.root, self)

        # Keypad section
        self.keypad_section = KeypadSection(self.root, self)

        # Key Configuration Panel
        self.config_panel = ConfigPanel(self.root, self)

        # Status Bar
        self.status_bar = StatusBar(self.root, self)
    
    def on_close(self):
        """Handle window close event.""" 
        # Stop status bar thread
        self.status_bar.stop()
        # Close the window
        self.root.destroy()
        
    def set_selected_profile(self, profile_index):
        """Set the currently selected profile."""
        self.selected_profile = profile_index
        self.status_bar.update_status(f"Selected Profile: {profile_index}")
        self.refresh_keypad()
        
    def set_selected_key(self, key_index):
        """Set the currently selected key."""
        self.selected_key = key_index
        self.status_bar.update_status(f"Selected Key: {key_index} on Profile: {self.selected_profile}")
        
    def refresh_keypad(self):
        """Refresh the keypad display based on current profile"""
        if hasattr(self, 'keypad_section'):
            self.keypad_section.update_keys(self.selected_profile)

if __name__ == "__main__":
    root = tk.Tk()
    app = MacroPadConfigurator(root)
    root.mainloop()