import tkinter as tk
import threading
import time
import os
import serial
import serial.tools.list_ports

# Import colors and ModernFrame if available
try:
    from main import COLORS, ModernFrame
except ImportError:
    # Fallback colors - modern dark theme
    COLORS = {
        "bg_dark": "#1E1E2E",     # Dark background
        "bg_medium": "#2A2A3C",   # Medium background for frames
        "bg_light": "#313244",    # Light background for elements
        "accent": "#89B4FA",      # Blue accent color
        "text": "#CDD6F4",        # Light text
        "text_dim": "#A6ADC8",    # Dimmed text
        "success": "#A6E3A1",     # Green for success
        "warning": "#F9E2AF",     # Yellow for warnings
        "error": "#F38BA8"        # Red for errors
    }
    
    # Simple ModernFrame implementation
    class ModernFrame(tk.Frame):
        def __init__(self, parent, **kwargs):
            self.corner_radius = kwargs.pop('corner_radius', 10)
            self.padding = kwargs.pop('padding', 0)
            super().__init__(parent, **kwargs)
            self.interior = self

class StatusBar:
    def __init__(self, root, app=None):
        self.root = root
        self.app = app
        self.connected = False
        self.device_port = None
        self.stop_thread = False  # Flag to control the connection check thread
        
        # Create modern status bar with rounded corners
        if 'ModernFrame' in globals():
            status_frame = ModernFrame(
                self.root, 
                corner_radius=15, 
                padding=5,
                bg=COLORS["bg_medium"], 
                highlightthickness=0
            )
        else:
            status_frame = tk.Frame(
                self.root, 
                bg=COLORS["bg_medium"], 
                bd=1, 
                relief="ridge"
            )
        
        status_frame.place(x=10, y=450, width=880, height=40)
        
        # Get interior frame reference
        interior = status_frame.interior if hasattr(status_frame, 'interior') else status_frame

        # Left frame for User Action status
        self.user_action_frame = tk.Frame(interior, bg=COLORS["bg_medium"])
        self.user_action_frame.pack(side="left", fill="both", expand=True)
        
        self.user_action_label = tk.Label(
            self.user_action_frame, 
            text="Status: Ready", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["warning"], 
            font=("Segoe UI", 10)
        )
        self.user_action_label.pack(side="left", padx=15)

        # Right frame for Connection Status
        self.connection_status_frame = tk.Frame(interior, bg=COLORS["bg_medium"])
        self.connection_status_frame.pack(side="right", fill="both", expand=True)
        
        self.connection_status_label = tk.Label(
            self.connection_status_frame, 
            text="Connection Status: Disconnected", 
            bg=COLORS["bg_medium"], 
            fg=COLORS["error"], 
            font=("Segoe UI", 10)
        )
        self.connection_status_label.pack(side="right", padx=15)
        
        # Start connection monitoring thread
        self.connection_thread = threading.Thread(target=self.check_connection_loop, daemon=True)
        self.connection_thread.start()
    
    def update_status(self, message):
        """Update the status bar with a message."""
        self.user_action_label.config(text=f"Status: {message}")
    
    def update_connection_status(self, connected, port=None):
        """Update the connection status display."""
        if connected:
            self.connection_status_label.config(
                text=f"Connection Status: Connected ({port})", 
                fg=COLORS["success"]
            )
            self.connected = True
            self.device_port = port
        else:
            self.connection_status_label.config(
                text="Connection Status: Disconnected", 
                fg=COLORS["error"]
            )
            self.connected = False
            self.device_port = None
    
    def check_connection(self):
        """Check if the device is connected."""
        try:
            # Look for common USB device identifiers for Arduino-based devices
            # Adjust these values based on your specific device
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                # Check for Raspberry Pi Pico device
                # Adjust the detection criteria based on your specific device
                if "Pico" in port.description or "USB Serial Device" in port.description:
                    try:
                        # Try to open the serial connection briefly to confirm it's working
                        ser = serial.Serial(port.device, 9600, timeout=1)
                        ser.close()
                        self.root.after(0, lambda: self.update_connection_status(True, port.device))
                        return True
                    except:
                        pass
            
            # No matching device found
            self.root.after(0, lambda: self.update_connection_status(False))
            return False
        except Exception as e:
            print(f"Error checking connection: {e}")
            self.root.after(0, lambda: self.update_connection_status(False))
            return False
    
    def check_connection_loop(self):
        """Continuously check for device connection in a separate thread."""
        while not self.stop_thread:
            self.check_connection()
            time.sleep(2)  # Check every 2 seconds
    
    def stop(self):
        """Stop the connection checking thread when closing the application."""
        self.stop_thread = True
        if self.connection_thread.is_alive():
            self.connection_thread.join(timeout=1)