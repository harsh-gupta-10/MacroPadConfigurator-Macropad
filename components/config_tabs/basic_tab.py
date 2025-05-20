import tkinter as tk
from tkinter import ttk
from .common import create_name_textbox, create_save_button

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
        self.tab_frame = tk.Frame(parent, bg="gray20")
        parent.add(self.tab_frame, text="Basic Config")
        
        # Create UI components
        self.create_ui()
    
    def create_ui(self):
        """Create the tab UI components."""
        # Name input box
        self.text_box = create_name_textbox(self.tab_frame)
        
        # Track text changes in this field
        self.text_box.bind("<KeyRelease>", lambda e: self.controller.update_shared_name(self.text_box))        # Category Dropdown (First Dropdown)
        tk.Label(self.tab_frame, text="Select Category", bg="gray20", fg="white", font=("Arial", 12)).pack(pady=1)
        self.key_category_var = tk.StringVar()
        self.key_category_var.set("Alphabets")  # Default Category

        category_dropdown = ttk.Combobox(self.tab_frame, textvariable=self.key_category_var, state="readonly")
        category_dropdown["values"] = ["Alphabets", "Numbers", "Symbols", "F1-F24", "Navigation Keys", 
                                    "Modifiers", "System Keys", "Media Keys", "Numpad Keys", "Other Keys"]
        category_dropdown.pack(pady=1)
          # Specific Keys Dropdown (Second Dropdown)
        tk.Label(self.tab_frame, text="Select Key", bg="gray20", fg="white", font=("Arial", 12)).pack(pady=1)
        self.specific_keys_var = tk.StringVar()
        self.specific_keys_dropdown = ttk.Combobox(self.tab_frame, textvariable=self.specific_keys_var, state="readonly")
        self.specific_keys_dropdown.pack(pady=1)

        # Update the second dropdown based on the selected category
        self.update_specific_keys()
        category_dropdown.bind("<<ComboboxSelected>>", self.update_specific_keys)

        # Save Button
        self.save_button = create_save_button(self.tab_frame, self.controller.save_config)
    
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
