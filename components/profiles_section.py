import tkinter as tk
from engine import load_profiles

class ProfilesSection:
    def __init__(self, root, app=None):
        self.root = root
        self.app = app  # Reference to main app
        
        profile_frame = tk.Frame(self.root, bg="gray15", bd=2, relief="ridge")
        profile_frame.place(x=10, y=70, width=180, height=370)

        tk.Label(profile_frame, text="Profiles", bg="gray15", fg="white", font=("Arial", 14, "bold"), pady=10).pack()
        
        self.profile_buttons = []
        profiles = load_profiles()
        profile_names = {
            "0": "Default", 
            "1": "VSCode", 
            "2": "OBS", 
            "3": "Software", 
            "4": "Windows", 
            "5": "Photoshop"
        }
        
        for profile_id in sorted(profiles.keys()):
            name = profile_names.get(profile_id, f"Profile {profile_id}")
            btn = tk.Button(profile_frame, text=name, bg="gray25", fg="white", relief="groove",
                            font=("Arial", 10, "bold"), activebackground="green", activeforeground="white",
                            command=lambda p=profile_id: self.select_profile(p))
            btn.pack(fill="x", padx=5, pady=3)
            self.profile_buttons.append((profile_id, btn))

    def select_profile(self, profile):
        """Handle profile selection."""
        # Update button appearance
        for profile_id, btn in self.profile_buttons:
            if profile_id == profile:
                btn.config(bg="green", fg="white")
            else:
                btn.config(bg="gray25", fg="white")
                
        # Update the app's selected profile
        if self.app:
            self.app.set_selected_profile(profile)