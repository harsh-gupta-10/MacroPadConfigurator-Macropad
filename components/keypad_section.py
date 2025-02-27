import tkinter as tk
from engine import load_profiles

class KeypadSection:
    def __init__(self, root, app=None):
        self.root = root
        self.app = app  # Reference to main app
        
        self.keypad_frame = tk.Frame(self.root, bg="gray25", bd=2, relief="ridge")
        self.keypad_frame.place(x=200, y=70, width=350, height=370)
        
        tk.Label(self.keypad_frame, text="Keypad", bg="gray25", fg="white", 
                font=("Arial", 14, "bold"), pady=5).grid(row=0, column=0, columnspan=3)
        
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
        
        # Create new buttons
        for i in range(9):
            key_num = str(i + 1)
            btn = tk.Button(self.keypad_frame, text=f"Key {key_num}", bg="gray30", fg="white", relief="raised",
                        font=("Arial", 8, "bold"), activebackground="red", activeforeground="white",
                        command=lambda k=key_num: self.configure_key(k),
                        width=10, height=3)
            btn.grid(row=(i // 3) + 1, column=i % 3, padx=10, pady=10)
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
                key_text = f"{name}\n[{' + '.join(keys)}]"
                btn.config(text=key_text)
            else:
                btn.config(text=f"Key {key_num}\n[Not Configured]")

    def configure_key(self, key):
        """Handle key configuration."""
        if self.app:
            self.app.set_selected_key(key)