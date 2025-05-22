import tkinter as tk
from tkinter import ttk
from .common import create_name_textbox, create_save_button

class TextConfigTab:
    def __init__(self, parent, controller):
        """
        Initialize the Text Config Tab
        
        Args:
            parent: Parent widget (tab control)
            controller: Reference to the main ConfigPanel for callbacks
        """
        self.parent = parent
        self.controller = controller
        
        # Create tab frame
        self.tab_frame = tk.Frame(parent, bg="gray20")
        parent.add(self.tab_frame, text="Text")
        
        # Create UI components
        self.create_ui()
    
    def create_ui(self):
        """Create the tab UI components."""
        # Name input box
        self.text_box = create_name_textbox(self.tab_frame, label_text="Name:")
        
        # Track text changes in this field
        self.text_box.bind("<KeyRelease>", lambda e: self.controller.update_shared_name(self.text_box))        # Radio buttons for text input type
        self.text_input_var = tk.StringVar(value="single")
        text_radio_frame = tk.Frame(self.tab_frame, bg="gray20")
        text_radio_frame.pack(pady=1)
        
        tk.Radiobutton(text_radio_frame, text="Single Line", variable=self.text_input_var, value="single", 
                      bg="gray20", fg="white", selectcolor="gray30", 
                      command=self.update_text_box).pack(side="left", padx=20)
        tk.Radiobutton(text_radio_frame, text="Paragraph", variable=self.text_input_var, value="paragraph", 
                      bg="gray20", fg="white", selectcolor="gray30",
                      command=self.update_text_box).pack(side="left", padx=20)
          # Text content frame with limited height
        self.text_content_frame = tk.Frame(self.tab_frame, bg="gray20")
        self.text_content_frame.pack(pady=1, fill="both", expand=False)
        
        # Initial text box (will be recreated based on radio button selection)        self.current_text_box = None
        self.update_text_box()
        
        # Save Button for Text tab - placed in its own frame to ensure visibility
        save_button_frame = tk.Frame(self.tab_frame, bg="gray20")
        save_button_frame.pack(side="bottom", pady=1, fill="x")
          # Use create_save_button to maintain consistency
        self.save_button = create_save_button(save_button_frame, self.controller.save_text_config)
        
        # Register save button with controller
        if hasattr(self.controller, 'register_save_button'):
            self.controller.register_save_button(self.save_button)
    
    def update_text_box(self):
        """Update the text box based on selected option (single line or paragraph)."""
        # Clear the existing frame
        for widget in self.text_content_frame.winfo_children():
            widget.destroy()
          # Create appropriate text box based on selection
        if self.text_input_var.get() == "single":
            self.current_text_box = tk.Text(self.text_content_frame, height=1.5, width=30, 
                                          wrap="none", bg="gray30", fg="white", font=("Arial", 10))
            self.current_text_box.pack(pady=2, fill="x", padx=10)
            
            # Add a label explaining the purpose
            tk.Label(self.text_content_frame, text="Single line of text to type", 
                    bg="gray20", fg="light gray", font=("Arial", 8)).pack(pady=1)
        else:  # paragraph
            # Use a shorter paragraph text box (height=5 instead of 8)
            self.current_text_box = tk.Text(self.text_content_frame, height=5, width=30, 
                                          wrap="word", bg="gray30", fg="white", font=("Arial", 10))
            self.current_text_box.pack(pady=2, fill="both", expand=False, padx=10)
            
            # Add scrollbar for paragraph text box
            scrollbar = tk.Scrollbar(self.text_content_frame)
            scrollbar.pack(side="right", fill="y")
            
            # Connect scrollbar to text box
            self.current_text_box.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.current_text_box.yview)
            
            # Add a label explaining the purpose
            tk.Label(self.text_content_frame, text="Multiple lines of text to type", 
                    bg="gray20", fg="light gray", font=("Arial", 8)).pack(pady=2)
    
    def get_config(self):
        """Get configuration data from this tab."""
        name = self.text_box.get("1.0", "end-1c").strip()
        text_content = self.current_text_box.get("1.0", "end-1c")
        
        if self.text_input_var.get() == "single":
            key_combination = [text_content.strip()]
        else:
            key_combination = [text_content]
        
        return name, key_combination, {}
    
    def get_text_config(self):
        """Get text-specific configuration data."""
        name = self.text_box.get("1.0", "end-1c").strip()
        text_content = self.current_text_box.get("1.0", "end-1c")
        
        # Create extra data for text type
        extra_data = {
            "software": None,  # Remove any software configuration
            "text_type": self.text_input_var.get(),
            "text_content": text_content
        }
        
        # For text input, we don't need a key combination, so we'll use a special identifier
        key_combination = ["text_input"]
        
        return name, key_combination, extra_data
    
    def set_name(self, name):
        """Set the name in the textbox."""
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", name)
