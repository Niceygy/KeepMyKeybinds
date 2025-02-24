import tkinter as tk
from tkinter import messagebox, font
import subprocess
import os
import shutil
import datetime
from fontTools.ttLib import TTFont
import requests


# Variables
CONFIG_LOCATION = "C:\\Users\\" + os.getlogin() + "\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\"

KEYBIND_FOLDER = CONFIG_LOCATION + "Bindings\\"

SERVICE_ENABLED = False

DATA_FOLDER = "C:\\Users\\" + os.getlogin() + "\\.KeepMyKeybinds\\"
BACKUP_FOLDER = DATA_FOLDER + "backups\\"
window = tk.Tk()


"""
Config
"""

def get_config():
    try:
        with open(f"{DATA_FOLDER}/config.txt", "r") as f:
            data = f.read()
            data = data.splitlines()
            for i in range(len(data)):
                line = data[i]
                key = line.split("=")[0]
                data = line.split("=")[1]
                match key:
                    case "ServiceEnabled":
                        break
        f.close()
    except FileNotFoundError as e:
        open(f"{DATA_FOLDER}/config.txt", "w").write("ServiceEnabled=False")
    except Exception as e:
        print(e)

get_config()

"""
Cosmetic
"""


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
    
"""
Startup
"""

# Init startup logic
try:
    if not os.path.exists(DATA_FOLDER):
        print("Creating APPDATA_LOCATION")
        os.mkdir(DATA_FOLDER)
    if not os.path.exists(BACKUP_FOLDER):
        print("Creating TEMP_FOLDER_LOCATION")
        os.mkdir(BACKUP_FOLDER)
    custom_font_family = register_custom_font(window, "EUROCAPS.TTF")
    print("Directories created successfully")
except Exception as e:
    print("Error on startup:", e)

"""
Backup/Restore
"""

def Backup():
    try:
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        folder_name = f"{date}_{time.hour}_{time.minute}"
        shutil.copytree(KEYBIND_FOLDER, os.path.join(BACKUP_FOLDER, "Bindings", folder_name))
        messagebox.showinfo("KeepMyKeybinds", f"Backup saved to folder under '{folder_name}'")
    except Exception as e:
        print("Error copying folders:", e)
        messagebox.showinfo("KeepMyKeybinds", e)

def Restore():
    print("Restoring")
    listdir = os.listdir(os.path.join(BACKUP_FOLDER, "Bindings"))
    listdir.sort()
    latest_backup = listdir[len(listdir)-1]
    choice = messagebox.askokcancel("KeepMyKeybinds!", f"Restore backup from {latest_backup}?")
    if choice:
        shutil.rmtree(KEYBIND_FOLDER)
        shutil.copytree(os.path.join(BACKUP_FOLDER, "Bindings", latest_backup), KEYBIND_FOLDER)
        messagebox.showinfo("KeepMyKeybinds!", "Sucessfully restored keybinds. Original backup has been kept")
    else:
        return

def OpenBackupLocation():
    print(f"Opening backup location: " + DATA_FOLDER)
    subprocess.Popen(rf'explorer /select,"{BACKUP_FOLDER}"')

"""
GUI
"""
window.title("Keep My Keybinds!")
window.geometry("300x380")
window.iconbitmap("icon.ico")
window.configure(bg='black')

title = tk.Label(text="Keep My Keybinds!", anchor="center", fg="#f07b05", bg="black", font=("Euro Caps", 20) ).pack(fill='x')

tk.Label(text="A simple utility for managing keybinds \nfor elite. With 🩷 & 💥, by niceygy.", fg="#f07b05", bg="black").pack(fill='x')

# BACKUP! & RESTORE! Button
BackupBtn = tk.Button(text="Manual Backup", fg="#f07b05", bg="black", command=Backup).pack(fill='x')

RestoreBtn = tk.Button(text="Manual Restore", fg="#f07b05", bg="black", command=Restore).pack(fill='x')

OpenBackupBtn = tk.Button(text="Open backup Location", fg="#f07b05", bg="black", command=OpenBackupLocation).pack(fill="x")

ServiceBtn = tk.Button(text="Background Backup & Restore", fg="#f07b05", bg="black").pack(fill="x")
tk.Label(text="This will run a background task on\n your device, that checks for \nchanges to the keybinds file.\nWhen it detects a change, it\n will make a backup copy", fg="#f07b05", bg="black", anchor="center").pack(fill="x")
tk.Label(text=f"(The service is {"enabled" if SERVICE_ENABLED else "disabled"})", fg="#f07b05", bg="black").pack(fill="x")

"""
Go!
"""

window.mainloop()