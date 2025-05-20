import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from engine import update_profile_key
import os

class ConfigPanel:
    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app  # Reference to main app
        self.create_ui()

    def create_ui(self):
        """Create the key changer panel."""
        config_frame = tk.Frame(self.parent, bg="gray25", bd=2, relief="ridge")
        config_frame.place(x=570, y=70, width=300, height=400)

        tk.Label(config_frame, text="Key Changer Panel", bg="gray25", fg="white", font=("Arial", 14, "bold"), pady=5).pack()

        self.tab_control = ttk.Notebook(config_frame)  # Save as instance variable
        self.tab_control.pack(expand=1, fill="both")

        # Tab for Basic Configuration
        basic_tab = tk.Frame(self.tab_control, bg="gray20")
        self.tab_control.add(basic_tab, text="Basic Config")

        # Name Input Box at the top
        self.text_box_label = tk.Label(basic_tab, text="Name(Use):", bg="gray20", fg="white", font=("Arial", 12))
        self.text_box_label.pack(pady=5)

        self.text_box = tk.Text(basic_tab, height=1.2, width=30, wrap="word", bg="gray30", fg="white", font=("Arial", 10))
        self.text_box.pack(pady=5)

        # Category Dropdown (First Dropdown)
        tk.Label(basic_tab, text="Select Category", bg="gray20", fg="white", font=("Arial", 12)).pack(pady=5)
        self.key_category_var = tk.StringVar()
        self.key_category_var.set("Alphabets")  # Default Category

        category_dropdown = ttk.Combobox(basic_tab, textvariable=self.key_category_var, state="readonly")
        category_dropdown["values"] = ["Alphabets", "Numbers", "Symbols", "F1-F24", "Navigation Keys", 
                                       "Modifiers", "System Keys", "Media Keys", "Numpad Keys", "Other Keys"]
        category_dropdown.pack(pady=5)
        
        # Specific Keys Dropdown (Second Dropdown)
        tk.Label(basic_tab, text="Select Key", bg="gray20", fg="white", font=("Arial", 12)).pack(pady=5)
        self.specific_keys_var = tk.StringVar()
        self.specific_keys_dropdown = ttk.Combobox(basic_tab, textvariable=self.specific_keys_var, state="readonly")
        self.specific_keys_dropdown.pack(pady=5)

        # Update the second dropdown based on the selected category
        self.update_specific_keys()
        category_dropdown.bind("<<ComboboxSelected>>", self.update_specific_keys)

        # Save Button
        save_button = tk.Button(basic_tab, text="Save", bg="blue", fg="white", font=("Arial", 12), command=self.save_config)
        save_button.pack(pady=10)

        # Tab for Advanced Configuration
        advanced_tab = tk.Frame(self.tab_control, bg="gray20")
        self.tab_control.add(advanced_tab, text="Advanced")

        # Name input box at the top
        self.advanced_text_label = tk.Label(advanced_tab, text="Name(Use):", bg="gray20", fg="white", font=("Arial", 12))
        self.advanced_text_label.pack(pady=5)

        self.advanced_text_box = tk.Text(advanced_tab, height=1.2, width=30, wrap="word", bg="gray30", fg="white", font=("Arial", 10))
        self.advanced_text_box.pack(pady=10)

        # Radio buttons for key combination options
        self.key_combo_var = tk.IntVar(value=2)
        radio_frame = tk.Frame(advanced_tab, bg="gray20")
        radio_frame.pack(pady=5)
        
        tk.Radiobutton(radio_frame, text="2 Keys", variable=self.key_combo_var, value=2, 
                      bg="gray20", fg="white", selectcolor="gray30", 
                      command=self.update_key_dropdowns).pack(side="left", padx=20)
        tk.Radiobutton(radio_frame, text="3 Keys", variable=self.key_combo_var, value=3, 
                      bg="gray20", fg="white", selectcolor="gray30",
                      command=self.update_key_dropdowns).pack(side="left", padx=20)

        # Frame for Dropdowns
        self.dropdown_frame = tk.Frame(advanced_tab, bg="gray20")
        self.dropdown_frame.pack(pady=10)

        # First modifier dropdown
        self.first_modifier_label = tk.Label(self.dropdown_frame, text="First Modifier:", bg="gray20", fg="white")
        self.first_modifier_var = tk.StringVar(value="None")
        self.modifier_dropdown_1 = ttk.Combobox(
            self.dropdown_frame, textvariable=self.first_modifier_var, state="readonly",
            values=["None", "Ctrl", "Alt", "Shift","windows"]
        )

        # Second modifier dropdown (can't match first)
        self.second_modifier_label = tk.Label(self.dropdown_frame, text="Second Modifier:", bg="gray20", fg="white")
        self.second_modifier_var = tk.StringVar(value="None")
        self.modifier_dropdown_2 = ttk.Combobox(
            self.dropdown_frame, textvariable=self.second_modifier_var, state="readonly",
            values=["None", "Ctrl", "Alt", "Shift","windows"]
        )

        # Third dropdown (all keys)
        self.third_key_label = tk.Label(self.dropdown_frame, text="Key:", bg="gray20", fg="white")
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
            self.dropdown_frame, textvariable=self.third_key_var, state="readonly",
            values=all_keys
        )

        self.modifier_dropdown_1.bind("<<ComboboxSelected>>", self.sync_modifiers)
        self.modifier_dropdown_2.bind("<<ComboboxSelected>>", self.sync_modifiers)

        # Initialize dropdowns based on default radio selection
        self.update_key_dropdowns()

        # Save Button
        advanced_save_button = tk.Button(advanced_tab, text="Save", bg="blue", fg="white", font=("Arial", 12), command=self.save_config)
        advanced_save_button.pack(pady=10)

        # Tab for Software Configuration
        software_tab = tk.Frame(self.tab_control, bg="gray20")
        self.tab_control.add(software_tab, text="Software")

        # Name input box at the top
        self.software_text_label = tk.Label(software_tab, text="Name(Use):", bg="gray20", fg="white", font=("Arial", 12))
        self.software_text_label.pack(pady=5)

        self.software_text_box = tk.Text(software_tab, height=1.2, width=30, wrap="word", bg="gray30", fg="white", font=("Arial", 10))
        self.software_text_box.pack(pady=10)

        # Software selection dropdown
        tk.Label(software_tab, text="Select Software:", bg="gray20", fg="white", font=("Arial", 12)).pack(pady=5)
        self.software_var = tk.StringVar(value="notepad")
        common_software = [
            "notepad", "mspaint", "calc", "explorer", 
            "chrome", "firefox", "msedge", "vscode",
            "word", "excel", "powerpoint", "outlook",
            "discord", "spotify", "photoshop", "blender",
            "steam", "obs", "vlc", "cmd"
        ]
        
        self.software_dropdown = ttk.Combobox(software_tab, textvariable=self.software_var, state="readonly", values=common_software)
        self.software_dropdown.pack(pady=5)
        
        # Custom software path option
        custom_frame = tk.Frame(software_tab, bg="gray20")
        custom_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(custom_frame, text="Or Enter your Software name:", bg="gray20", fg="white").pack(anchor="w")
        
        path_frame = tk.Frame(custom_frame, bg="gray20")
        path_frame.pack(fill="x", pady=5)
        
        self.custom_path_var = tk.StringVar()
        self.custom_path_entry = tk.Entry(path_frame, textvariable=self.custom_path_var, bg="gray30", fg="white")
        self.custom_path_entry.pack(side="left", expand=True, fill="x", padx=(0,5))
        
        
        
        # Modifier key option (for software launch with hotkey)
        modifier_frame = tk.Frame(software_tab, bg="gray20")
        modifier_frame.pack(pady=10)
        
        tk.Label(modifier_frame, text="Type:", bg="gray20", fg="white").pack(side="left", padx=5)
        
        self.software_modifier_var = tk.StringVar(value="Software")
        ttk.Combobox(
            modifier_frame, textvariable=self.software_modifier_var, state="readonly",
            values=["Software"], width=10
        ).pack(side="left", padx=5)
        
        # Save Button
        software_save_button = tk.Button(software_tab, text="Save", bg="blue", fg="white", font=("Arial", 12), command=self.save_config)
        software_save_button.pack(pady=10)

        # Tab for Text Configuration
        text_tab = tk.Frame(self.tab_control, bg="gray20")
        self.tab_control.add(text_tab, text="Text")
        
        # Name input box at the top
        self.text_tab_name_label = tk.Label(text_tab, text="Name:", bg="gray20", fg="white", font=("Arial", 12))
        self.text_tab_name_label.pack(pady=5)
        
        self.text_tab_name_box = tk.Text(text_tab, height=1.2, width=30, wrap="word", bg="gray30", fg="white", font=("Arial", 10))
        self.text_tab_name_box.pack(pady=5)
        
        # Radio buttons for text input type
        self.text_input_var = tk.StringVar(value="single")
        text_radio_frame = tk.Frame(text_tab, bg="gray20")
        text_radio_frame.pack(pady=5)
        
        tk.Radiobutton(text_radio_frame, text="Single Line", variable=self.text_input_var, value="single", 
                      bg="gray20", fg="white", selectcolor="gray30", 
                      command=self.update_text_box).pack(side="left", padx=20)
        tk.Radiobutton(text_radio_frame, text="Paragraph", variable=self.text_input_var, value="paragraph", 
                      bg="gray20", fg="white", selectcolor="gray30",
                      command=self.update_text_box).pack(side="left", padx=20)
          # Text content frame with limited height
        self.text_content_frame = tk.Frame(text_tab, bg="gray20")
        self.text_content_frame.pack(pady=10, fill="both", expand=False)
        
        # Initial text box (will be recreated based on radio button selection)
        self.current_text_box = None
        self.update_text_box()
        
        # Save Button for Text tab - placed in its own frame to ensure visibility
        save_button_frame = tk.Frame(text_tab, bg="gray20")
        save_button_frame.pack(side="bottom", pady=10, fill="x")
        
        save_text_button = tk.Button(save_button_frame, text="Save", bg="blue", fg="white", font=("Arial", 12), 
                                    command=self.save_text_config)
        save_text_button.pack(pady=5)

    def browse_software(self):
        """Open file dialog to browse for executable"""
        file_path = filedialog.askopenfilename(
            title="Select Application",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if file_path:
            self.custom_path_var.set(file_path)
            # Also update the name if it's empty
            if not self.software_text_box.get("1.0", "end-1c").strip():
                app_name = os.path.splitext(os.path.basename(file_path))[0]
                self.software_text_box.delete("1.0", "end")
                self.software_text_box.insert("1.0", f"Open {app_name}")

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
        elif category == "Other Keys":            keys = ["Escape", "Space", "Backspace", "windows"]
        else:
            keys = []
        self.specific_keys_dropdown["values"] = keys
        if keys:
            self.specific_keys_var.set(keys[0])
        else:
            self.specific_keys_var.set("")
            
    def save_config(self):
        """Collect user input and update the key configuration."""
        # Get the currently selected profile and key
        if not hasattr(self.app, 'selected_profile') or not hasattr(self.app, 'selected_key'):
            messagebox.showwarning("Selection Required", "Please select a profile and key first.")
            return
            
        profile_index = self.app.selected_profile
        key_index = self.app.selected_key
        
        # Get configuration from the active tab
        active_tab = self.tab_control.index("current")  # Get the current tab index
        
        # Initialize extra_data with software field explicitly set to None
        # This ensures any previous software configuration is removed
        extra_data = {"software": None}
        
        if active_tab == 0:  # Basic tab
            specific_key = self.specific_keys_var.get()
            name = self.text_box.get("1.0", "end-1c").strip()
            key_combination = [specific_key.lower()]
            # Using extra_data with software:None to remove any existing software configuration
        elif active_tab == 1:  # Advanced tab
            num_keys = self.key_combo_var.get()
            name = self.advanced_text_box.get("1.0", "end-1c").strip()
            # Using extra_data with software:None to remove any existing software configuration
            
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
        elif active_tab == 2:  # Software tab
            name = self.software_text_box.get("1.0", "end-1c").strip()
            # Use custom path if provided, otherwise use selected software
            if self.custom_path_var.get().strip():
                software = self.custom_path_var.get().strip()
            else:
                software = self.software_var.get()
                
            # Add modifier key if selected
            if self.software_modifier_var.get() != "None":
                key_combination = [self.software_modifier_var.get().lower()]
            else:
                key_combination = []
            
            # For software tab, set the software field
            extra_data["software"] = software
        else:  # Text tab
            name = self.text_tab_name_box.get("1.0", "end-1c").strip()
            if self.text_input_var.get() == "single":
                text_content = self.current_text_box.get("1.0", "end-1c").strip()
                key_combination = [text_content]
            else:
                text_content = self.current_text_box.get("1.0", "end-1c").strip()
                key_combination = [text_content]

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
        
        # Get the name and text content
        name = self.text_tab_name_box.get("1.0", "end-1c").strip()
        text_content = self.current_text_box.get("1.0", "end-1c")
        
        # Create extra data for text type
        extra_data = {
            "software": None,  # Remove any software configuration
            "text_type": self.text_input_var.get(),
            "text_content": text_content
        }
        
        # For text input, we don't need a key combination, so we'll use a special identifier
        key_combination = ["text_input"]
        
        # Update the key configuration
        if update_profile_key(profile_index, key_index, key_combination, name, extra_data):
            messagebox.showinfo("Success", f"Text configuration for Key {key_index} updated in profile {profile_index}")
            
            # Update UI to show the new configuration
            if hasattr(self.app, 'refresh_keypad'):
                self.app.refresh_keypad()

    def update_text_box(self):
        """Update the text box based on selected option (single line or paragraph)."""
        # Clear the existing frame
        for widget in self.text_content_frame.winfo_children():
            widget.destroy()
        
        # Create appropriate text box based on selection
        if self.text_input_var.get() == "single":
            self.current_text_box = tk.Text(self.text_content_frame, height=1.5, width=30, 
                                          wrap="none", bg="gray30", fg="white", font=("Arial", 10))
            self.current_text_box.pack(pady=5, fill="x", padx=10)
            
            # Add a label explaining the purpose
            tk.Label(self.text_content_frame, text="Single line of text to type", 
                    bg="gray20", fg="light gray", font=("Arial", 8)).pack(pady=2)
        else:  # paragraph
            # Use a shorter paragraph text box (height=5 instead of 8)
            self.current_text_box = tk.Text(self.text_content_frame, height=5, width=30, 
                                          wrap="word", bg="gray30", fg="white", font=("Arial", 10))
            self.current_text_box.pack(pady=5, fill="both", expand=False, padx=10)
            
            # Add scrollbar for paragraph text box
            scrollbar = tk.Scrollbar(self.text_content_frame)
            scrollbar.pack(side="right", fill="y")
            
            # Connect scrollbar to text box
            self.current_text_box.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.current_text_box.yview)
            
            # Add a label explaining the purpose
            tk.Label(self.text_content_frame, text="Multiple lines of text to type", 
                    bg="gray20", fg="light gray", font=("Arial", 8)).pack(pady=2)

    def get_selected_profile(self):
        """
        Return the selected profile index. 
        Update mapping as needed for your profile buttons.
        """
        # Example mapping of profile names to indices based on your keyout.py
        profile_map = {
            "Default": 0,
            "Photoshop": 5,   # Adjust if needed
            "Pre Pro": 2,     # ...
            "Blender": 3,
            "Custom-1": 4,
            "Custom-2": 1
        }
        # Currently hardcoded to "Default" or you could store the selected profile from ProfilesSection
        return profile_map.get("Default", 0)

    def sync_modifiers(self, event=None):
        """Sample logic for sync. Not strictly required unless you're handling advanced combos."""
        first = self.first_modifier_var.get()
        second = self.second_modifier_var.get()
        options = ["None", "Ctrl", "Alt", "Shift", "windows"]  # Added "windows" to the options
        
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
        """Update the dropdown configuration based on radio button selection"""
        num_keys = self.key_combo_var.get()
        
        # Reset all dropdowns
        for widget in self.dropdown_frame.winfo_children():
            widget.pack_forget()
        
        if num_keys == 2:
            # Show only 2 dropdowns (first modifier and main key)
            self.first_modifier_var.set("None")
            self.second_modifier_var.set("None")
            
            # First key (modifier)
            self.first_modifier_label.pack(pady=(5,0))
            self.modifier_dropdown_1.pack(pady=(0,5))
            
            # Second key (main key)
            self.third_key_label.pack(pady=(5,0))
            self.third_dropdown.pack(pady=(0,5))
            
        else:  # num_keys == 3
            # Show all 3 dropdowns
            self.first_modifier_var.set("None")
            self.second_modifier_var.set("None")
            
            # First modifier
            self.first_modifier_label.pack(pady=(5,0))
            self.modifier_dropdown_1.pack(pady=(0,5))
            
            # Second modifier
            self.second_modifier_label.pack(pady=(5,0))
            self.modifier_dropdown_2.pack(pady=(0,5))
            
            # Main key
            self.third_key_label.pack(pady=(5,0))
            self.third_dropdown.pack(pady=(0,5))

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigPanel(root)
    root.mainloop()