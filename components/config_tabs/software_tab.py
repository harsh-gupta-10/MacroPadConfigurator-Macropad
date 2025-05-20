import tkinter as tk
import os
from tkinter import ttk, filedialog
from .common import create_name_textbox, create_save_button

class SoftwareConfigTab:
    def __init__(self, parent, controller):
        """
        Initialize the Software Config Tab
        
        Args:
            parent: Parent widget (tab control)
            controller: Reference to the main ConfigPanel for callbacks
        """
        self.parent = parent
        self.controller = controller
        
        # Create tab frame
        self.tab_frame = tk.Frame(parent, bg="gray20")
        parent.add(self.tab_frame, text="Software")
        
        # Create UI components
        self.create_ui()
    
    def create_ui(self):
        """Create the tab UI components."""
        # Name input box
        self.text_box = create_name_textbox(self.tab_frame)
        
        # Track text changes in this field
        self.text_box.bind("<KeyRelease>", lambda e: self.controller.update_shared_name(self.text_box))        # Software selection dropdown
        tk.Label(self.tab_frame, text="Select Software:", bg="gray20", fg="white", font=("Arial", 12)).pack(pady=1)
        self.software_var = tk.StringVar(value="notepad")
        common_software = [
            "notepad", "mspaint", "calc", "explorer", 
            "chrome", "firefox", "msedge", "vscode",
            "word", "excel", "powerpoint", "outlook",
            "discord", "spotify", "photoshop", "blender",
            "steam", "obs", "vlc", "cmd"
        ]
        
        self.software_dropdown = ttk.Combobox(self.tab_frame, textvariable=self.software_var, state="readonly", values=common_software)
        self.software_dropdown.pack(pady=1)          # Custom software path option
        custom_frame = tk.Frame(self.tab_frame, bg="gray20")
        custom_frame.pack(pady=1, fill="x", padx=20)
        
        tk.Label(custom_frame, text="Or Enter your Software name:", bg="gray20", fg="white").pack(anchor="w")
        
        path_frame = tk.Frame(custom_frame, bg="gray20")
        path_frame.pack(fill="x", pady=2)
        
        self.custom_path_var = tk.StringVar()
        self.custom_path_entry = tk.Entry(path_frame, textvariable=self.custom_path_var, bg="gray30", fg="white")
        self.custom_path_entry.pack(side="left", expand=True, fill="x", padx=(0,5))
        
        browse_button = tk.Button(path_frame, text="Browse...", bg="gray40", fg="white", command=self.browse_software)
        browse_button.pack(side="right")          # Modifier key option (for software launch with hotkey)
        modifier_frame = tk.Frame(self.tab_frame, bg="gray20")
        modifier_frame.pack(pady=1)
        
        tk.Label(modifier_frame, text="Type:", bg="gray20", fg="white").pack(side="left", padx=5)
        
        self.software_modifier_var = tk.StringVar(value="Software")
        ttk.Combobox(
            modifier_frame, textvariable=self.software_modifier_var, state="readonly",
            values=["Software"], width=10
        ).pack(side="left", padx=5)
        
        # Save Button
        self.save_button = create_save_button(self.tab_frame, self.controller.save_config)
    
    def get_config(self):
        """Get configuration data from this tab."""
        name = self.text_box.get("1.0", "end-1c").strip()
        
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
        
        # Extra data with software field
        extra_data = {"software": software}
        
        return name, key_combination, extra_data
    
    def set_name(self, name):
        """Set the name in the textbox."""
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", name)
    
    def browse_software(self):
        """Open file dialog to browse for executable."""
        file_path = filedialog.askopenfilename(
            title="Select Application",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if file_path:
            self.custom_path_var.set(file_path)
            # Also update the name if it's empty
            if not self.text_box.get("1.0", "end-1c").strip():
                app_name = os.path.splitext(os.path.basename(file_path))[0]
                self.text_box.delete("1.0", "end")
                self.text_box.insert("1.0", f"Open {app_name}")
                # Update shared name
                self.controller.update_shared_name(self.text_box)
