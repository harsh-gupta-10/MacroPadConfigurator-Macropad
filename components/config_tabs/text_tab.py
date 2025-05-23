import tkinter as tk
from tkinter import ttk
from .common import create_name_textbox, create_save_button, COLORS

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
        self.tab_frame = tk.Frame(parent, bg=COLORS["bg_medium"])
        parent.add(self.tab_frame, text="Text")
        
        # Create UI components
        self.create_ui()
    
    def create_ui(self):
        """Create the tab UI components."""
        # Name input box
        self.text_box = create_name_textbox(self.tab_frame, label_text="Name:")
        
        # Track text changes in this field
        self.text_box.bind("<KeyRelease>", lambda e: self.controller.update_shared_name(self.text_box))        # Create a spacer
        spacer = tk.Frame(self.tab_frame, height=5, bg=COLORS["bg_medium"])
        spacer.pack(fill="x")
        
        # Radio buttons for text input type
        self.text_input_var = tk.StringVar(value="single")
        text_radio_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        text_radio_frame.pack(pady=5)
        
        # Modern styling for radio buttons
        radio_bg = COLORS["bg_medium"]
        radio_fg = COLORS["text"]
        radio_select = COLORS["bg_light"]
        radio_active_bg = COLORS["selection"]
        radio_font = ("Segoe UI", 10)
        
        tk.Radiobutton(text_radio_frame, text="Single Line", variable=self.text_input_var, value="single", 
                      bg=radio_bg, fg=radio_fg, selectcolor=radio_select, 
                      activebackground=radio_active_bg, activeforeground=radio_fg,
                      font=radio_font,
                      command=self.update_text_box).pack(side="left", padx=20)
                      
        tk.Radiobutton(text_radio_frame, text="Paragraph", variable=self.text_input_var, value="paragraph", 
                      bg=radio_bg, fg=radio_fg, selectcolor=radio_select,
                      activebackground=radio_active_bg, activeforeground=radio_fg,
                      font=radio_font,
                      command=self.update_text_box).pack(side="left", padx=20)        # Add a separator line
        separator = tk.Frame(self.tab_frame, height=1, bg=COLORS["bg_light"])
        separator.pack(fill="x", padx=10, pady=5)
          # Text content frame with modern styling - with a fixed maximum height
        self.text_content_frame = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"])
        self.text_content_frame.pack(pady=3, fill="both", expand=False, padx=10)
        
        # Initial text box (will be recreated based on radio button selection)
        self.current_text_box = None
        self.update_text_box()        # Create a bottom container to ensure save button visibility
        bottom_container = tk.Frame(self.tab_frame, bg=COLORS["bg_medium"], height=50)
        bottom_container.pack(side="bottom", fill="x", pady=0)
        bottom_container.pack_propagate(False)  # Prevent children from changing the frame size
        
        # Add a separator line before save button for visual clarity
        separator = tk.Frame(bottom_container, height=1, bg=COLORS["bg_light"])
        separator.pack(fill="x", padx=10, pady=2)

        # Save Button for Text tab - placed in its own frame to ensure visibility
        save_button_frame = tk.Frame(bottom_container, bg=COLORS["bg_medium"])
        save_button_frame.pack(fill="x")
        
        # Save Button with modern styling - centered
        button_container = create_save_button(save_button_frame, self.controller.save_text_config)
        button_container.pack(side="top", pady=5, padx=0, anchor="center")
        
        # Access the button through the container's button attribute
        self.save_button = button_container.button
        
        # Register save button with controller
        if hasattr(self.controller, 'register_save_button'):
            self.controller.register_save_button(self.save_button)
    def update_text_box(self):
        """Update the text box based on selected option (single line or paragraph)."""
        # Clear the existing frame
        for widget in self.text_content_frame.winfo_children():
            widget.destroy()
            
        # Label for text input
        tk.Label(
            self.text_content_frame, 
            text="Text to Send:", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["accent"],
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(0,2))
        
        # Create modern styled text frame with border and adaptive height constraint
        if self.text_input_var.get() == "single":
            frame_height = 60  # Increased height for 2-line single input
        else:
            frame_height = 120  # Larger height for paragraph input
            
        text_frame = tk.Frame(
            self.text_content_frame, 
            bg=COLORS["bg_light"], 
            bd=0, 
            highlightthickness=1,
            highlightbackground=COLORS["selection"], 
            highlightcolor=COLORS["accent"],
            height=frame_height  # Adaptive height based on input mode
        )
        # Use propagate=False to enforce the height constraint
        text_frame.pack_propagate(False)
        text_frame.pack(pady=2, fill="both", expand=False)
          # Create appropriate text box based on selection
        if self.text_input_var.get() == "single":
            self.current_text_box = tk.Text(
                text_frame, 
                height=2,  # Set to exactly 2 lines height
                width=30, 
                wrap="word",  # Use word wrap for better text flow in 2 lines
                bg=COLORS["bg_light"], 
                fg=COLORS["text"], 
                font=("Segoe UI", 10),
                bd=0,
                padx=5,
                pady=2,
                insertbackground=COLORS["accent"]  # Cursor color
            )
            self.current_text_box.pack(pady=5, fill="x", padx=5, expand=True)  # Increased padding and allow expansion
              # Add a label explaining the purpose
            tk.Label(
                self.text_content_frame, 
                text="Short text to type (up to 2 lines)", 
                bg=COLORS["bg_medium"], 
                fg=COLORS["text_dim"], 
                font=("Segoe UI", 8, "italic")
            ).pack(pady=1, anchor="w")
        
        else:  # paragraph            # Use a shorter paragraph text box with modern styling and fixed height
            self.current_text_box = tk.Text(
                text_frame, 
                height=4,  # Reduced height to ensure save button visibility
                width=30, 
                wrap="word", 
                bg=COLORS["bg_light"], 
                fg=COLORS["text"], 
                font=("Segoe UI", 10),
                bd=0,
                padx=5,
                pady=2,
                insertbackground=COLORS["accent"]  # Cursor color
            )
            self.current_text_box.pack(pady=2, fill="both", expand=False, padx=2)
            
            # Add scrollbar for paragraph text box with modern styling
            scrollbar = tk.Scrollbar(
                text_frame,
                bg=COLORS["bg_medium"],
                troughcolor=COLORS["bg_dark"],
                activebackground=COLORS["accent"]
            )
            scrollbar.pack(side="right", fill="y")
            
            # Connect scrollbar to text box
            self.current_text_box.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.current_text_box.yview)
            
            # Add a label explaining the purpose
            tk.Label(
                self.text_content_frame, 
                text="Multiple lines of text to type", 
                bg=COLORS["bg_medium"], 
                fg=COLORS["text_dim"], 
                font=("Segoe UI", 8, "italic")
            ).pack(pady=2, anchor="w")
    
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
