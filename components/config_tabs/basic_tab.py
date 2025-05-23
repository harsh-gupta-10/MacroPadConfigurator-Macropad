import tkinter as tk
from tkinter import ttk
from .common import create_name_textbox, create_save_button, COLORS

class BasicConfigTab:
    def __init__(self, parent, controller):
        """
        Initialize the Basic Config Tab
        
        Args:
            parent: Parent widget (tab control)
            controller: Reference to the main ConfigPanel for callbacks
        """
        self.parent = parent
        self.controller = controller
        
        # Create tab frame
        self.tab_frame = tk.Frame(parent, bg=COLORS["bg_medium"])
        parent.add(self.tab_frame, text="Basic Config")
        
        # Create UI components
        self.create_ui()
    def create_ui(self):
        """Create the tab UI components."""
        # Name input box
        self.text_box = create_name_textbox(self.tab_frame)
        
        # Track text changes in this field
        self.text_box.bind("<KeyRelease>", lambda e: self.controller.update_shared_name(self.text_box))
        
        # Create a spacer
        spacer = tk.Frame(self.tab_frame, height=5, bg=COLORS["bg_medium"])
        spacer.pack(fill="x")
        
        # Category Dropdown (First Dropdown)
        # Create a container frame for better layout
        category_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        category_frame.pack(fill="x", padx=10, pady=3)
        
        tk.Label(
            category_frame, 
            text="Select Category", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"], 
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(2,0))
        
        self.key_category_var = tk.StringVar()
        self.key_category_var.set("Alphabets")  # Default Category

        category_dropdown = ttk.Combobox(
            category_frame, 
            textvariable=self.key_category_var, 
            state="readonly",
            style="TCombobox"
        )
        category_dropdown["values"] = ["Alphabets", "Numbers", "Symbols", "F1-F24", "Navigation Keys", 
                                    "Modifiers", "System Keys", "Media Keys", "Numpad Keys", "Other Keys"]
        category_dropdown.pack(fill="x", pady=1)
        
        # Specific Keys Dropdown (Second Dropdown)
        # Create a container frame for better layout
        keys_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        keys_frame.pack(fill="x", padx=10, pady=3)
        
        tk.Label(
            keys_frame, 
            text="Select Key", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"], 
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(2,0))
        
        self.specific_keys_var = tk.StringVar()
        self.specific_keys_dropdown = ttk.Combobox(
            keys_frame, 
            textvariable=self.specific_keys_var, 
            state="readonly",
            style="TCombobox"
        )
        self.specific_keys_dropdown.pack(fill="x", pady=1)        # Update the second dropdown based on the selected category
        self.update_specific_keys()
        category_dropdown.bind("<<ComboboxSelected>>", self.update_specific_keys)        # Add a spacer frame to push content up and save button down
        spacer = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        spacer.pack(fill="both", expand=True)
        
        # Add a separator line before save button for visual clarity
        separator = tk.Frame(self.tab_frame, height=1, bg=COLORS["bg_light"])
        separator.pack(fill="x", padx=10, pady=8, side="bottom")
            # Save Button - placed in its own frame at the bottom for consistency
        save_button_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        save_button_frame.pack(side="bottom", pady=5, fill="x")
        
        # Save Button with modern styling - centered
        button_container = create_save_button(save_button_frame, self.controller.save_config)
        button_container.pack(side="top", pady=5, padx=0, anchor="center")
        
        # Access the button through the container's button attribute
        self.save_button = button_container.button
        
        # Register save button with controller
        if hasattr(self.controller, 'register_save_button'):
            self.controller.register_save_button(self.save_button)
    
    def update_specific_keys(self, event=None):
        """Update the specific keys dropdown based on the selected category."""
        category = self.key_category_var.get()
        if category == "Alphabets":
            keys = [chr(i) for i in range(65, 91)]  # A-Z
        elif category == "Numbers":
            keys = [str(i) for i in range(10)]
        elif category == "Symbols":
            keys = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "{", 
                   "}", "[", "]", "|", "\\", ":", ";", '"', "'", "<", ">", ",", ".", "?", "/"]
        elif category == "F1-F24":
            keys = [f"F{i}" for i in range(1, 25)]
        elif category == "Navigation Keys":
            keys = ["Up", "Down", "Left", "Right", "Home", "End", "Page Up", "Page Down"]
        elif category == "Modifiers":
            keys = ["Shift", "Ctrl", "Alt", "Caps Lock", "Tab"]
        elif category == "System Keys":
            keys = ["Insert", "Delete", "Print Screen", "Scroll Lock", "Pause/Break"]
        elif category == "Media Keys":
            keys = ["Volume Up", "Volume Down", "Mute", "Play/Pause", "Stop", "Next Track", "Previous Track"]
        elif category == "Numpad Keys":
            keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "Enter", "Decimal"]
        elif category == "Other Keys":            
            keys = ["Escape", "Space", "Backspace", "windows"]
        else:
            keys = []
        self.specific_keys_dropdown["values"] = keys
        if keys:
            self.specific_keys_var.set(keys[0])
        else:
            self.specific_keys_var.set("")
    
    def get_config(self):
        """Get configuration data from this tab."""
        name = self.text_box.get("1.0", "end-1c").strip()
        specific_key = self.specific_keys_var.get()
        key_combination = [specific_key.lower()]
        return name, key_combination, {}  # name, key_combination, extra_data
    
    def set_name(self, name):
        """Set the name in the textbox."""
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", name)
