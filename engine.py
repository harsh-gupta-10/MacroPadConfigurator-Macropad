import json
import os
import sys
from tkinter import messagebox

def get_json_path():
    """Always use the keysfile.json from the O: drive"""
    # Define the path to keysfile.json on the O: drive
    o_drive_path = "O:\\keysfile.json"
    
    # Check if the O: drive is accessible
    if os.path.exists("O:\\"):
        # Create the file if it doesn't exist
        if not os.path.exists(o_drive_path):
            try:
                # Create a default empty structure
                default_data = {"profiles": {}}
                for i in range(6):  # 6 profiles (0-5)
                    default_data["profiles"][str(i)] = {}
                    for j in range(1, 10):  # 9 keys (1-9)
                        default_data["profiles"][str(i)][str(j)] = {}
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(o_drive_path), exist_ok=True)
                
                # Write default JSON
                with open(o_drive_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, indent=2)
            except Exception as e:
                print(f"Error creating default keysfile.json: {e}")
        return o_drive_path
    else:
        # O: drive isn't available, show an error message
        print("O: drive not accessible. Please make sure the drive is connected.")
        try:
            messagebox.showerror("Drive Error", 
                                "O: drive not accessible.\nPlease make sure the drive is connected.")
        except:
            # If running without GUI
            pass
            
        # Return a path to a local copy as fallback
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(__file__)
        return os.path.join(base_dir, "keysfile.json")

def update_profile_key(profile_index, key_index, new_keys, name=None, extra_data=None):
    """
    Update a specific key in a profile within keysfile.json
    
    Args:
        profile_index: The profile number as string (e.g., "0", "1", etc)
        key_index: The key number as string (e.g., "1", "2", etc)
        new_keys: List of key combinations (e.g., ["ctrl", "s"])
        name: Optional name for the shortcut
        extra_data: Dictionary of additional data (e.g., {"software": "notepad"})
    """
    keysfile_path = get_json_path()
    try:
        # Load the current JSON data
        with open(keysfile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        profile_str = str(profile_index)  # Convert to string if it's an int
        key_str = str(key_index)  # Convert to string if it's an int
        
        # Check if profile exists
        if profile_str not in data["profiles"]:
            print(f"Profile {profile_str} not found")
            return False
            
        # Check if key exists in profile
        if key_str not in data["profiles"][profile_str]:
            # Create new key entry if it doesn't exist
            data["profiles"][profile_str][key_str] = {"name": name or "Custom Shortcut", "key": []}
        else:
            # If key exists, keep only the basic fields to reset previous configuration
            data["profiles"][profile_str][key_str] = {
                "name": data["profiles"][profile_str][key_str].get("name", "Custom Shortcut"),
                "key": data["profiles"][profile_str][key_str].get("key", [])
            }
        
        # Update the key combination
        data["profiles"][profile_str][key_str]["key"] = new_keys
        
        # Update the name if provided
        if name:
            data["profiles"][profile_str][key_str]["name"] = name
            
        # Add any extra data fields
        if extra_data:
            for key, value in extra_data.items():
                if value is None:
                    # If value is None, remove this field if it exists
                    if key in data["profiles"][profile_str][key_str]:
                        del data["profiles"][profile_str][key_str][key]
                else:
                    # Otherwise set or update the field
                    data["profiles"][profile_str][key_str][key] = value
            
        # Save the updated JSON
        with open(keysfile_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"Updated key {key_str} in profile {profile_str}")
        return True
        
    except Exception as e:
        print(f"Error updating keysfile.json: {e}")
        return False

def load_profiles():
    """Load all profiles from keysfile.json"""
    keysfile_path = get_json_path()
    try:
        with open(keysfile_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["profiles"]
    except Exception as e:
        print(f"Error loading profiles: {e}")
        return {}