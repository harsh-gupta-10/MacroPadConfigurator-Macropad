import tkinter as tk
from tkinter import ttk, messagebox
from engine import update_profile_key, load_profiles

# Import our new tab modules
from .config_tabs.basic_tab import BasicConfigTab
from .config_tabs.advanced_tab import AdvancedConfigTab
from .config_tabs.software_tab import SoftwareConfigTab
from .config_tabs.text_tab import TextConfigTab

class ConfigPanel:
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app  # Reference to main app
        self.shared_name = ""  # Shared name variable for all tabs
        self.tab_modules = []  # References to tab modules
        self.save_buttons = []  # Track all save buttons
        self.create_ui()
        
    def create_ui(self):
        """Create the key changer panel."""
        config_frame = tk.Frame(self.parent, bg="gray25", bd=2, relief="ridge")
        config_frame.place(x=570, y=10, width=300, height=430)

        tk.Label(config_frame, text="Key Changer Panel", bg="gray25", fg="white", font=("Arial", 14, "bold"), pady=0).pack()

        # Create the tab control
        self.tab_control = ttk.Notebook(config_frame)
        self.tab_control.pack(expand=1, fill="both")
        
        # Set up event handling for tab change
        self.tab_control.bind("<<NotebookTabChanged>>", self.sync_name_fields)

        # Create all tab modules
        self.basic_tab = BasicConfigTab(self.tab_control, self)
        self.advanced_tab = AdvancedConfigTab(self.tab_control, self)
        self.software_tab = SoftwareConfigTab(self.tab_control, self)
        self.text_tab = TextConfigTab(self.tab_control, self)
        
        # Store references to tabs for iteration
        self.tab_modules = [self.basic_tab, self.advanced_tab, self.software_tab, self.text_tab]
        
        # Set up loaded profile/key information if available
        self.load_key_data()
        
        # Initialize save buttons to disabled (since no key is selected initially)
        self.update_save_buttons()
    
    def update_shared_name(self, source_textbox):
        """Update the shared name variable from the source textbox and update all other textboxes."""
        # Get the current name from the source textbox
        self.shared_name = source_textbox.get("1.0", "end-1c").strip()
        
        # Update name in all tabs
        for tab in self.tab_modules:
            # Check if the source is not from this tab
            if hasattr(tab, 'text_box') and tab.text_box != source_textbox:
                tab.set_name(self.shared_name)
    
    def sync_name_fields(self, event=None):
        """Sync name fields when tabs are changed."""
        # Get current tab
        current_tab = self.tab_control.index("current")
        
        # Set the current key name in the active tab's name field
        if current_tab < len(self.tab_modules):
            self.tab_modules[current_tab].set_name(self.shared_name)
    
    def load_key_data(self):
        """Load the key data when a key is selected."""
        if self.app and hasattr(self.app, 'selected_profile') and hasattr(self.app, 'selected_key'):
            profile_index = self.app.selected_profile
            key_index = self.app.selected_key
            
            # Load profiles
            profiles = load_profiles()
            
            if profile_index in profiles and key_index in profiles[profile_index]:
                key_config = profiles[profile_index][key_index]
                name = key_config.get("name", f"Key {key_index}")
                
                # Set shared name
                self.shared_name = name
                
                # Update all name fields
                for tab in self.tab_modules:
                    tab.set_name(name)
                    
            # Enable save buttons when a key is selected
            self.update_save_buttons()
    
    def save_config(self):
        """Collect user input and update the key configuration."""
        # Get the currently selected profile and key
        if not hasattr(self.app, 'selected_profile') or not hasattr(self.app, 'selected_key'):
            messagebox.showwarning("Selection Required", "Please select a profile and key first.")
            return
            
        profile_index = self.app.selected_profile
        key_index = self.app.selected_key
        
        # Get configuration from the active tab
        active_tab_index = self.tab_control.index("current")
        
        # Default extra_data with software field set to None
        extra_data = {"software": None}
        
        # Get configuration from the active tab
        active_tab = self.tab_modules[active_tab_index]
        name, key_combination, tab_extra_data = active_tab.get_config()
        
        # Add tab-specific extra data
        extra_data.update(tab_extra_data)
        
        # Use the shared name
        name = self.shared_name
        
        # Update the key configuration
        if update_profile_key(profile_index, key_index, key_combination, name, extra_data):
            messagebox.showinfo("Success", f"Key {key_index} updated in profile {profile_index}")
            
            # Update UI to show the new configuration
            if hasattr(self.app, 'refresh_keypad'):
                self.app.refresh_keypad()
        else:
            messagebox.showerror("Error", "Failed to update key configuration")
    
    def save_text_config(self):
        """Save the text configuration to the selected key."""
        # Get the currently selected profile and key
        if not hasattr(self.app, 'selected_profile') or not hasattr(self.app, 'selected_key'):
            messagebox.showwarning("Selection Required", "Please select a profile and key first.")
            return
            
        profile_index = self.app.selected_profile
        key_index = self.app.selected_key
        
        # Get text config data
        name, key_combination, extra_data = self.text_tab.get_text_config()
        
        # Use the shared name
        name = self.shared_name
        
        # Update the key configuration
        if update_profile_key(profile_index, key_index, key_combination, name, extra_data):
            messagebox.showinfo("Success", f"Text configuration for Key {key_index} updated in profile {profile_index}")
            
            # Update UI to show the new configuration
            if hasattr(self.app, 'refresh_keypad'):
                self.app.refresh_keypad()
        else:
            messagebox.showerror("Error", "Failed to update text configuration")
    
    def register_save_button(self, button):
        """Register a save button to be enabled/disabled based on key selection."""
        if button and button not in self.save_buttons:
            self.save_buttons.append(button)
        
    def update_save_buttons(self):
        """Update the state of all save buttons based on key selection."""
        state = "normal" if self.app and hasattr(self.app, 'selected_key') and self.app.selected_key else "disabled"
        for button in self.save_buttons:
            button.config(state=state)
