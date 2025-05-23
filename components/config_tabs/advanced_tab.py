import tkinter as tk
from tkinter import ttk
from .common import create_name_textbox, create_save_button, COLORS

class AdvancedConfigTab:
    def __init__(self, parent, controller):
        """
        Initialize the Advanced Config Tab
        
        Args:
            parent: Parent widget (tab control)
            controller: Reference to the main ConfigPanel for callbacks
        """
        self.parent = parent
        self.controller = controller
        
        # Create tab frame
        self.tab_frame = tk.Frame(parent, bg=COLORS["bg_medium"])
        parent.add(self.tab_frame, text="Advanced")
        
        # Create UI components
        self.create_ui()
    
    def create_ui(self):
        """Create the tab UI components."""
        # Name input box
        self.text_box = create_name_textbox(self.tab_frame)
        
        # Track text changes in this field        self.text_box.bind("<KeyRelease>", lambda e: self.controller.update_shared_name(self.text_box))
        
        # Create a spacer
        spacer = tk.Frame(self.tab_frame, height=5, bg=COLORS["bg_medium"])
        spacer.pack(fill="x")
        
        # Radio buttons for key combination options
        self.key_combo_var = tk.IntVar(value=2)
        radio_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        radio_frame.pack(pady=5)
        
        # Modern styling for radio buttons
        radio_bg = COLORS["bg_medium"]
        radio_fg = COLORS["text"]
        radio_select = COLORS["bg_light"]
        radio_active_bg = COLORS["selection"]
        radio_font = ("Segoe UI", 10)
        
        tk.Radiobutton(radio_frame, text="2 Keys", variable=self.key_combo_var, value=2, 
                      bg=radio_bg, fg=radio_fg, selectcolor=radio_select, 
                      activebackground=radio_active_bg, activeforeground=radio_fg,
                      font=radio_font,
                      command=self.update_key_dropdowns).pack(side="left", padx=20)
                      
        tk.Radiobutton(radio_frame, text="3 Keys", variable=self.key_combo_var, value=3, 
                      bg=radio_bg, fg=radio_fg, selectcolor=radio_select,
                      activebackground=radio_active_bg, activeforeground=radio_fg,
                      font=radio_font,
                      command=self.update_key_dropdowns).pack(side="left", padx=20)        # Frame for Dropdowns with modern styling
        self.dropdown_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        self.dropdown_frame.pack(pady=5, padx=10, fill="x")

        # First modifier dropdown
        self.first_modifier_label = tk.Label(
            self.dropdown_frame, 
            text="First Modifier:", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"],
            font=("Segoe UI", 11)
        )
        self.first_modifier_var = tk.StringVar(value="None")
        self.modifier_dropdown_1 = ttk.Combobox(
            self.dropdown_frame, 
            textvariable=self.first_modifier_var, 
            state="readonly",
            style="TCombobox",
            values=["None", "Ctrl", "Alt", "Shift", "windows"]
        )        # Second modifier dropdown (can't match first)
        self.second_modifier_label = tk.Label(
            self.dropdown_frame, 
            text="Second Modifier:", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"],
            font=("Segoe UI", 11)
        )
        self.second_modifier_var = tk.StringVar(value="None")
        self.modifier_dropdown_2 = ttk.Combobox(
            self.dropdown_frame, 
            textvariable=self.second_modifier_var, 
            state="readonly",
            style="TCombobox",
            values=["None", "Ctrl", "Alt", "Shift", "windows"]
        )

        # Third dropdown (all keys)
        self.third_key_label = tk.Label(
            self.dropdown_frame, 
            text="Key:", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"],
            font=("Segoe UI", 11)
        )
        self.third_key_var = tk.StringVar()
        all_keys = (
            [chr(i) for i in range(65, 91)] +  # A-Z
            [str(i) for i in range(10)] +      # 0-9
            ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "{",
             "}", "[", "]", "|", "\\", ":", ";", '"', "'", "<", ">", ",", ".", "?", "/"] +
            [f"F{i}" for i in range(1, 25)] +  # F1-F24
            ["Up", "Down", "Left", "Right", "Home", "End", "Page Up", "Page Down"] +  # Navigation
            ["Shift", "Ctrl", "Alt", "Caps Lock", "Tab"] +  # Modifiers
            ["Insert", "Delete", "Print Screen", "Scroll Lock", "Pause/Break"] +  # System Keys
            ["Volume Up", "Volume Down", "Mute", "Play/Pause", "Stop", "Next Track", "Previous Track"] +  # Media Keys
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] +  # Numpad Numbers
            ["+", "-", "*", "/", "Enter", "Decimal"] +  # Numpad Operators
            ["Escape", "Space", "Backspace"] +  # Other Keys
            ["windows"]  # Add more keys as needed
        )
        self.third_dropdown = ttk.Combobox(
            self.dropdown_frame,
            textvariable=self.third_key_var,
            state="readonly",
            style="TCombobox",
            values=all_keys
        )

        self.modifier_dropdown_1.bind("<<ComboboxSelected>>", self.sync_modifiers)
        self.modifier_dropdown_2.bind("<<ComboboxSelected>>", self.sync_modifiers)        # Initialize dropdowns based on default radio selection
        self.update_key_dropdowns()
          # Add a spacer frame to push content up and save button down
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
    
    def get_config(self):
        """Get configuration data from this tab."""
        name = self.text_box.get("1.0", "end-1c").strip()
        num_keys = self.key_combo_var.get()
        
        if num_keys == 2:
            # 2-key combination
            modifiers = []
            if self.first_modifier_var.get() != "None":
                modifiers.append(self.first_modifier_var.get().lower())
                
            main_key = self.third_key_var.get().lower()
            key_combination = modifiers + [main_key]
        else:
            # 3-key combination
            modifiers = []
            if self.first_modifier_var.get() != "None":
                modifiers.append(self.first_modifier_var.get().lower())
            if self.second_modifier_var.get() != "None":
                modifiers.append(self.second_modifier_var.get().lower())
                
            main_key = self.third_key_var.get().lower()
            key_combination = modifiers + [main_key]
        
        return name, key_combination, {}  # name, key_combination, extra_data
    
    def set_name(self, name):
        """Set the name in the textbox."""
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", name)
    
    def sync_modifiers(self, event=None):
        """Synchronize modifiers to prevent duplicates."""
        first = self.first_modifier_var.get()
        second = self.second_modifier_var.get()
        options = ["None", "Ctrl", "Alt", "Shift", "windows"]
        
        if first != "None" and second == first:
            self.second_modifier_var.set("None")
        
        second_options = options.copy()
        if first != "None" and first in second_options:
            second_options.remove(first)
        self.modifier_dropdown_2["values"] = second_options

        first_options = options.copy()
        if second != "None" and second in first_options:
            first_options.remove(second)
        self.modifier_dropdown_1["values"] = first_options
    
    def update_key_dropdowns(self):
        """Update the dropdown configuration based on radio button selection."""
        num_keys = self.key_combo_var.get()
        
        # Reset all dropdowns
        for widget in self.dropdown_frame.winfo_children():
            widget.pack_forget()
        
        if num_keys == 2:
            # Show only 2 dropdowns (first modifier and main key)
            self.first_modifier_var.set("None")
            self.second_modifier_var.set("None")            # First key (modifier)
            self.first_modifier_label.pack(pady=(1,0))
            self.modifier_dropdown_1.pack(pady=(0,1))
              # Second key (main key)
            self.third_key_label.pack(pady=(1,0))
            self.third_dropdown.pack(pady=(0,1))
            
        else:  # num_keys == 3
            # Show all 3 dropdowns
            self.first_modifier_var.set("None")
            self.second_modifier_var.set("None")
              # First modifier
            self.first_modifier_label.pack(pady=(1,0))
            self.modifier_dropdown_1.pack(pady=(0,1))
              # Second modifier
            self.second_modifier_label.pack(pady=(1,0))
            self.modifier_dropdown_2.pack(pady=(0,1))
            
            # Main key
            self.third_key_label.pack(pady=(1,0))
            self.third_dropdown.pack(pady=(0,1))
