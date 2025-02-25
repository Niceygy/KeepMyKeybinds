import tkinter as tk
from tkinter import messagebox, font
import subprocess
import os
import shutil
import datetime
from fontTools.ttLib import TTFont
import webbrowser

# Variables
ED_KEYBINDS_FOLDER = (
    "C:\\Users\\"
    + os.getlogin()
    + "\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\Bindings\\"
)
DATA_FOLDER = f"C:\\Users\\{os.getlogin()}\\.KeepMyKeybinds\\"
BACKUP_FOLDER = DATA_FOLDER + "backups\\"
DEBUG_ENABLED = False
DEBUG_FOLDER = DATA_FOLDER + "debug\\"
DEVENV = False

#GUI Init

window = tk.Tk()
ToggleTrayBtn = None
window.title("Keep My Keybinds!")
window.geometry("340x380")
window.iconbitmap("icon.ico")
window.configure(bg="black")


def log(message: str, func: str):
    try:
        if DEVENV:
            print(f"{func}: {message}")
        elif DEBUG_ENABLED:
            with open(f"{DEBUG_FOLDER}/debug.txt", "a") as f:
                f.write(f"{func}: {message}\n")
                f.close()
    except FileNotFoundError:
        os.mkdir(DEBUG_FOLDER)
        open(f"{DEBUG_FOLDER}/debug.txt", "w").write("\n")


#Config


def get_config():
    global DEBUG_ENABLED  # Add this line
    try:
        with open(f"{DATA_FOLDER}/config.txt", "r") as f:
            data = f.read()
            data = data.splitlines()
            for i in range(len(data)):
                line = data[i]
                print(line)
                if line.startswith("#"):
                    continue
                key = line.split("=")[0]
                print(key == "DebugEnabled")
                data = line.split("=")[1]
                match key:
                    case "KeybindPath":
                        ED_KEYBINDS_FOLDER = data
                        log(f"KeybindPath: {data}", "get_config")
                    case "DebugEnabled":
                        if data == "True":
                            DEBUG_ENABLED = True
                        else:
                            DEBUG_ENABLED = False
                        log(f"DebugEnabled: {data}", "get_config")

        f.close()
    except FileNotFoundError as e:
        open(f"{DATA_FOLDER}/config.txt", "w").write(f"KeybindPath={ED_KEYBINDS_FOLDER}\nDebugEnabled=False")
        log("Config folder made", "get_config")
    except Exception as e:
        log(e, "get_config")

#Cosmetic



# Function to list font families within a font file
def list_font_families(font_path):
    font = TTFont(font_path)
    families = [name.toUnicode() for name in font["name"].names if name.nameID == 1]
    return families


# Function to register a custom font
def register_custom_font(root, font_path):
    font_families = list_font_families(font_path)

    if font_families:
        # Register the first font family
        custom_font_family = font_families[0]
        root.tk.call(
            "font",
            "create",
            custom_font_family,
            "-family",
            custom_font_family,
            "-size",
            12,
        )

        # Set the registered font as default for the application
        default_font = font.Font(family=custom_font_family, size=12)
        root.option_add("*Font", default_font)

        return custom_font_family
    else:
        raise ValueError("No font families found in the font file.")

#Backup/Restore


def Backup():
    try:
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()
        folder_name = f"{date}_{time.hour}_{time.minute}"
        shutil.copytree(
            ED_KEYBINDS_FOLDER, os.path.join(BACKUP_FOLDER, "Bindings", folder_name)
        )
        messagebox.showinfo(
            "KeepMyKeybinds", f"Backup saved to folder under '{folder_name}'"
        )
    except Exception as e:
        log(f"Error copying folders: {e}", "Backup")
        messagebox.showinfo("KeepMyKeybinds", e)


def Restore():
    log("Restoring", "Restore")
    listdir = os.listdir(os.path.join(BACKUP_FOLDER, "Bindings"))
    listdir.sort()
    latest_backup = listdir[len(listdir) - 1]
    log(f"Asked user if they want backup from {latest_backup}", "Restore")
    choice = messagebox.askokcancel(
        "KeepMyKeybinds!", f"Restore backup from {latest_backup}?"
    )
    if choice:
        shutil.rmtree(ED_KEYBINDS_FOLDER)
        shutil.copytree(
            os.path.join(BACKUP_FOLDER, "Bindings", latest_backup), ED_KEYBINDS_FOLDER
        )
        messagebox.showinfo(
            "KeepMyKeybinds!",
            "Sucessfully restored keybinds. Original backup has been kept",
        )
    else:
        return


def OpenBackupLocation():
    log(f"Opening backup location: {DATA_FOLDER}", "OpenBackupLocation")
    subprocess.Popen(rf'explorer /select,"{BACKUP_FOLDER}"')

def OpenHelpPage():
    log("Opening help page", "OpenHelpPage")
    webbrowser.open_new_tab("https://niceygy.net/keepmykeybinds")


# Init startup logic
try:
    if not os.path.exists(DATA_FOLDER):
        log(f"Creating Data Folder at {DATA_FOLDER}", "Startup")
        os.mkdir(DATA_FOLDER)
    if not os.path.exists(BACKUP_FOLDER):
        log(f"Creating BACKUP_FOLDER at {BACKUP_FOLDER}", "Startup")
        os.mkdir(BACKUP_FOLDER)
    if not os.path.exists(DEBUG_FOLDER) and DEBUG_ENABLED:
        log(f"Creating DEBUG_FOLDER at {DEBUG_FOLDER}", "Startup")
        os.mkdir(DEBUG_FOLDER)
    custom_font_family = register_custom_font(window, "EUROCAPS.TTF")
    get_config()
    if os.path.exists(os.path.join(os.getcwd(), ".gitignore")):
        DEBUG_ENABLED = True
        DEVENV = True
except Exception as e:
    log(e, "Startup")


#GUI Conf
title = tk.Label(
    text="Keep My Keybinds!",
    anchor="center",
    fg="#f07b05",
    bg="black",
    font=("Euro Caps", 20),
).pack(fill="x")

tk.Label(
    text="A simple utility for managing keybinds \nfor elite. With 🩷 & 💥, by niceygy.",
    fg="#f07b05",
    bg="black",
    font=("Euro Caps", 13),
).pack(fill="x")

# BACKUP! & RESTORE! Button
BackupBtn = tk.Button(
    text="Manual Backup",
    fg="#f07b05",
    bg="black",
    command=Backup,
    font=("Euro Caps", 13),
).pack(fill="x")

RestoreBtn = tk.Button(
    text="Manual Restore",
    fg="#f07b05",
    bg="black",
    command=Restore,
    font=("Euro Caps", 13),
).pack(fill="x")

# Open Backup Folder
OpenBackupBtn = tk.Button(
    text="Open backup Location",
    fg="#f07b05",
    bg="black",
    command=OpenBackupLocation,
    font=("Euro Caps", 13),
).pack(fill="x")
tk.Label(
    text="Opens the backup folder \nin file explorer",
    fg="#f07b05",
    bg="black",
    anchor="center",
    font=("Euro Caps", 13),
).pack(fill="x")

OpenHelpBtn = tk.Button(
    text="Help Me!",
    fg="#f07b05",
    bg="black",
    command=OpenHelpPage,
    font=("Euro Caps", 13),
).pack(fill="x")
tk.Label(
    text="Opens the help page \nin a browser",
    fg="#f07b05",
    bg="black",
    anchor="center",
    font=("Euro Caps", 13),
).pack(fill="x")



#Go!

log("Startup Sucsess", "Main")
window.mainloop()
