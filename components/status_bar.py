import tkinter as tk

class StatusBar:
    def __init__(self, root):
        self.root = root

        status_frame = tk.Frame(self.root, bg="gray15", bd=1, relief="sunken")
        status_frame.place(x=10, y=460, width=880, height=40)

        # Left frame for User Action status
        self.user_action_frame = tk.Frame(status_frame, bg="gray15")
        self.user_action_frame.pack(side="left", fill="both", expand=True)
        self.user_action_label = tk.Label(self.user_action_frame, text="Status: Ready", bg="gray15", fg="yellow", font=("Arial", 10, "italic"))
        self.user_action_label.pack(side="left", padx=10)

        # Right frame for Connection Status
        self.connection_status_frame = tk.Frame(status_frame, bg="gray15")
        self.connection_status_frame.pack(side="right", fill="both", expand=True)
        self.connection_status_label = tk.Label(self.connection_status_frame, text="Connection Status: Disconnected", bg="gray15", fg="red", font=("Arial", 10, "italic"))
        self.connection_status_label.pack(side="right", padx=10)
    
    def update_status(self, message):
        """Update the status bar with a message."""
        self.user_action_label.config(text=f"Status: {message}")