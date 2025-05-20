import tkinter as tk
from tkinter import ttk

def create_name_textbox(parent, label_text="Name(Use):"):
    """Create a standardized name textbox with label."""
    frame = tk.Frame(parent, bg="gray20")
    frame.pack(pady=5, fill="x")
    
    label = tk.Label(frame, text=label_text, bg="gray20", fg="white", font=("Arial", 12))
    label.pack(pady=2)
    
    textbox = tk.Text(frame, height=1.2, width=30, wrap="word", bg="gray30", fg="white", font=("Arial", 10))
    textbox.pack(pady=2, fill="x", padx=10)
    
    return textbox

def create_save_button(parent, command, text="Save"):
    """Create a standardized save button."""
    save_button = tk.Button(parent, text=text, bg="blue", fg="white", font=("Arial", 12), command=command)
    save_button.pack(pady=10)
    return save_button
