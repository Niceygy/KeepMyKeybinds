import tkinter as tk
from tkinter import font
from fontTools.ttLib import TTFont

# Function to list font families within a font file
def list_font_families(font_path):
    font = TTFont(font_path)
    families = [name.toUnicode() for name in font['name'].names if name.nameID == 1]
    return families

# Function to register a custom font
def register_custom_font(root, font_path):
    font_families = list_font_families(font_path)
    
    if font_families:
        # Register the first font family
        custom_font_family = font_families[0]
        root.tk.call('font', 'create', custom_font_family, '-family', custom_font_family, '-size', 12)
        
        # Set the registered font as default for the application
        default_font = font.Font(family=custom_font_family, size=12)
        root.option_add("*Font", default_font)
        
        return custom_font_family
    else:
        raise ValueError("No font families found in the font file.")

root = tk.Tk()

# Path to the custom font file
font_path = "EuroCaps.ttf"

# Register and use the custom font
custom_font_family = register_custom_font(root, font_path)
label = tk.Label(root, text="Hello, Custom Font!")
label.pack()

root.mainloop()
