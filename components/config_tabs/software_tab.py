import tkinter as tk
import os
from tkinter import ttk, filedialog
from .common import create_name_textbox, create_save_button, COLORS

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
        self.tab_frame = tk.Frame(parent, bg=COLORS["bg_medium"])
        parent.add(self.tab_frame, text="Software")
        
        # Create UI components
        self.create_ui()
    
    def create_ui(self):
        """Create the tab UI components."""
        # Name input box
        self.text_box = create_name_textbox(self.tab_frame)
        
        # Track text changes in this field
        self.text_box.bind("<KeyRelease>", lambda e: self.controller.update_shared_name(self.text_box))        # Create a spacer
        spacer = tk.Frame(self.tab_frame, height=5, bg=COLORS["bg_medium"])
        spacer.pack(fill="x")
        
        # Create a container frame for better layout
        software_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        software_frame.pack(fill="x", padx=10, pady=3)
        
        # Software selection dropdown
        tk.Label(
            software_frame, 
            text="Select Software:", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"], 
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(2,0))
        
        self.software_var = tk.StringVar(value="notepad")
        common_software = [
            "notepad", "mspaint", "calc", "explorer", 
            "chrome", "firefox", "msedge", "vscode",
            "word", "excel", "powerpoint", "outlook",
            "discord", "spotify", "photoshop", "blender",
            "steam", "obs", "vlc", "cmd"
        ]
        
        self.software_dropdown = ttk.Combobox(
            software_frame, 
            textvariable=self.software_var, 
            state="readonly", 
            style="TCombobox",
            values=common_software
        )
        self.software_dropdown.pack(fill="x", pady=1)        # Add a separator line
        separator = tk.Frame(self.tab_frame, height=1, bg=COLORS["bg_light"])
        separator.pack(fill="x", padx=10, pady=8)
        
        # Custom software path option with modern styling
        custom_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        custom_frame.pack(pady=3, fill="x", padx=10)
        
        tk.Label(
            custom_frame, 
            text="Or Enter your Software name:", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"],
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(0,2))
        
        path_frame = tk.Frame(custom_frame, bg=COLORS["bg_medium"])
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
        ).pack(side="left", padx=5)        # Add a spacer frame to push content up and save button down
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
